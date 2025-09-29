#!/usr/bin/env python3
"""
Exiles Installer Link Validation Test Suite
Tests all URLs, GitHub repos, and winget packages in apps.json for validity
"""

import json
import requests
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
import subprocess

class LinkTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ExilesInstaller-LinkTester/1.0.0 (GitHub: github.com/exiles-team/installer)'
        })
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.github_api_calls = 0
        self.max_github_calls = 60  # Rate limit safety
        
    def load_apps_config(self):
        """Load apps.json configuration"""
        config_path = Path('src/apps.json')
        if not config_path.exists():
            print("❌ Error: src/apps.json not found")
            sys.exit(1)
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in apps.json: {e}")
            sys.exit(1)
    
    def test_http_url(self, url, app_name, method_type="direct"):
        """Test HTTP/HTTPS URL accessibility"""
        try:
            # Use HEAD request first for efficiency
            response = self.session.head(url, timeout=10, allow_redirects=True)
            
            # Some servers don't support HEAD, try GET if HEAD fails
            if response.status_code == 405:
                response = self.session.get(url, timeout=10, stream=True)
                # Close the stream immediately to save bandwidth
                response.close()
            
            if response.status_code == 200:
                self.results['passed'].append({
                    'app': app_name,
                    'url': url,
                    'method': method_type,
                    'status': response.status_code
                })
                return True
            elif response.status_code in [301, 302, 303, 307, 308]:
                # Redirects are usually okay
                self.results['warnings'].append({
                    'app': app_name,
                    'url': url,
                    'method': method_type,
                    'status': response.status_code,
                    'issue': f'Redirect to: {response.headers.get("Location", "unknown")}'
                })
                return True
            else:
                self.results['failed'].append({
                    'app': app_name,
                    'url': url,
                    'method': method_type,
                    'status': response.status_code,
                    'error': f'HTTP {response.status_code}'
                })
                return False
                
        except requests.exceptions.RequestException as e:
            self.results['failed'].append({
                'app': app_name,
                'url': url,
                'method': method_type,
                'status': None,
                'error': str(e)
            })
            return False
    
    def test_github_repo(self, repo, app_name, asset_pattern=None):
        """Test GitHub repository and release accessibility"""
        if self.github_api_calls >= self.max_github_calls:
            self.results['warnings'].append({
                'app': app_name,
                'url': f'https://github.com/{repo}',
                'method': 'github_api',
                'status': None,
                'issue': 'Skipped: GitHub API rate limit protection'
            })
            return True
            
        try:
            # Test repository exists
            api_url = f'https://api.github.com/repos/{repo}'
            response = self.session.get(api_url, timeout=10)
            self.github_api_calls += 1
            
            if response.status_code == 200:
                repo_data = response.json()
                
                # Test if repository has releases if asset pattern is provided
                if asset_pattern:
                    releases_url = f'https://api.github.com/repos/{repo}/releases/latest'
                    releases_response = self.session.get(releases_url, timeout=10)
                    self.github_api_calls += 1
                    
                    if releases_response.status_code == 200:
                        release_data = releases_response.json()
                        assets = release_data.get('assets', [])
                        
                        # Check if any asset matches the pattern
                        matching_assets = [asset for asset in assets 
                                         if asset_pattern.lower() in asset['name'].lower()]
                        
                        if matching_assets:
                            self.results['passed'].append({
                                'app': app_name,
                                'url': f'https://github.com/{repo}',
                                'method': 'github_api',
                                'status': 200,
                                'details': f'Found {len(matching_assets)} matching release assets'
                            })
                        else:
                            self.results['warnings'].append({
                                'app': app_name,
                                'url': f'https://github.com/{repo}',
                                'method': 'github_api',
                                'status': 200,
                                'issue': f'No assets matching "{asset_pattern}" in latest release'
                            })
                    else:
                        self.results['warnings'].append({
                            'app': app_name,
                            'url': f'https://github.com/{repo}',
                            'method': 'github_api',
                            'status': releases_response.status_code,
                            'issue': 'Repository exists but no releases found'
                        })
                else:
                    # Just testing repository existence
                    self.results['passed'].append({
                        'app': app_name,
                        'url': f'https://github.com/{repo}',
                        'method': 'github_api',
                        'status': 200,
                        'details': f'Repository active, {repo_data.get("stargazers_count", 0)} stars'
                    })
                
                return True
            elif response.status_code == 404:
                self.results['failed'].append({
                    'app': app_name,
                    'url': f'https://github.com/{repo}',
                    'method': 'github_api',
                    'status': 404,
                    'error': 'Repository not found or private'
                })
                return False
            else:
                self.results['failed'].append({
                    'app': app_name,
                    'url': f'https://github.com/{repo}',
                    'method': 'github_api',
                    'status': response.status_code,
                    'error': f'GitHub API error: {response.status_code}'
                })
                return False
                
        except requests.exceptions.RequestException as e:
            self.results['failed'].append({
                'app': app_name,
                'url': f'https://github.com/{repo}',
                'method': 'github_api',
                'status': None,
                'error': f'Network error: {str(e)}'
            })
            return False
    
    def test_winget_package(self, package_id, app_name):
        """Test winget package availability"""
        try:
            # Check if winget is available
            result = subprocess.run(['winget', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                self.results['warnings'].append({
                    'app': app_name,
                    'url': f'winget:{package_id}',
                    'method': 'winget',
                    'status': None,
                    'issue': 'Winget not available on this system'
                })
                return True  # Not a failure, just can't test
            
            # Search for the package
            search_result = subprocess.run(
                ['winget', 'search', package_id, '--exact'], 
                capture_output=True, text=True, timeout=30
            )
            
            if search_result.returncode == 0 and package_id in search_result.stdout:
                self.results['passed'].append({
                    'app': app_name,
                    'url': f'winget:{package_id}',
                    'method': 'winget',
                    'status': 0,
                    'details': 'Package found in winget repository'
                })
                return True
            else:
                self.results['failed'].append({
                    'app': app_name,
                    'url': f'winget:{package_id}',
                    'method': 'winget',
                    'status': search_result.returncode,
                    'error': 'Package not found in winget repository'
                })
                return False
                
        except subprocess.TimeoutExpired:
            self.results['failed'].append({
                'app': app_name,
                'url': f'winget:{package_id}',
                'method': 'winget',
                'status': None,
                'error': 'Winget command timed out'
            })
            return False
        except FileNotFoundError:
            self.results['warnings'].append({
                'app': app_name,
                'url': f'winget:{package_id}',
                'method': 'winget',
                'status': None,
                'issue': 'Winget not installed on this system'
            })
            return True  # Not a failure, just can't test
        except Exception as e:
            self.results['failed'].append({
                'app': app_name,
                'url': f'winget:{package_id}',
                'method': 'winget',
                'status': None,
                'error': f'Winget error: {str(e)}'
            })
            return False
    
    def test_app_links(self, app):
        """Test all links for a single application"""
        app_name = app.get('name', 'Unknown')
        app_id = app.get('id', 'unknown')
        
        print(f"🔍 Testing {app_name} ({app_id})...")
        
        # Test legacy single install_type URLs
        if 'install_type' in app:
            install_type = app['install_type']
            
            if install_type == 'web' and 'url' in app:
                self.test_http_url(app['url'], app_name, 'web_link')
            elif install_type in ['exe', 'zip', 'msi'] and 'url' in app:
                self.test_http_url(app['url'], app_name, install_type)
            elif install_type == 'github':
                # Handle legacy GitHub entries
                github_repo = app.get('github_repo')
                github_asset = app.get('github_asset')
                if github_repo:
                    self.test_github_repo(github_repo, app_name, github_asset)
            elif install_type == 'winget':
                # Handle legacy winget entries  
                winget_id = app.get('winget_id')
                if winget_id:
                    self.test_winget_package(winget_id, app_name)
        
        # Test new install_methods array
        if 'install_methods' in app:
            for method in app['install_methods']:
                method_type = method.get('type', 'unknown')
                
                if method_type == 'winget':
                    winget_id = method.get('winget_id')
                    if winget_id:
                        self.test_winget_package(winget_id, app_name)
                
                elif method_type == 'github':
                    github_repo = method.get('github_repo')
                    github_asset = method.get('github_asset')
                    if github_repo:
                        self.test_github_repo(github_repo, app_name, github_asset)
                
                elif method_type in ['exe', 'zip', 'msi', 'web']:
                    url = method.get('url')
                    if url:
                        self.test_http_url(url, app_name, method_type)
        
        # Add small delay to be respectful to servers
        time.sleep(0.5)
    
    def run_tests(self):
        """Run all link validation tests"""
        print("🚀 Starting Exiles Installer Link Validation Test Suite")
        print("=" * 60)
        
        config = self.load_apps_config()
        apps = config.get('apps', [])
        
        print(f"📊 Found {len(apps)} applications to test")
        print()
        
        for i, app in enumerate(apps, 1):
            print(f"[{i}/{len(apps)}] ", end="")
            self.test_app_links(app)
        
        self.print_results()
    
    def print_results(self):
        """Print comprehensive test results"""
        print()
        print("=" * 60)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results['passed']) + len(self.results['failed']) + len(self.results['warnings'])
        
        print(f"✅ PASSED: {len(self.results['passed'])}")
        print(f"❌ FAILED: {len(self.results['failed'])}")
        print(f"⚠️  WARNINGS: {len(self.results['warnings'])}")
        print(f"📊 TOTAL: {total_tests}")
        print()
        
        # Print failed tests (most important)
        if self.results['failed']:
            print("❌ FAILED TESTS (Need Immediate Attention):")
            print("-" * 50)
            for failure in self.results['failed']:
                print(f"   {failure['app']}")
                print(f"   🔗 {failure['url']}")
                print(f"   📄 Method: {failure['method']}")
                print(f"   ❌ Error: {failure['error']}")
                if failure['status']:
                    print(f"   📊 Status: {failure['status']}")
                print()
        
        # Print warnings (attention needed)
        if self.results['warnings']:
            print("⚠️  WARNINGS (Review Recommended):")
            print("-" * 50)
            for warning in self.results['warnings']:
                print(f"   {warning['app']}")
                print(f"   🔗 {warning['url']}")
                print(f"   📄 Method: {warning['method']}")
                print(f"   ⚠️  Issue: {warning['issue']}")
                if warning['status']:
                    print(f"   📊 Status: {warning['status']}")
                print()
        
        # Print successful tests summary
        if self.results['passed']:
            print("✅ SUCCESSFUL TESTS:")
            print("-" * 50)
            method_counts = {}
            for success in self.results['passed']:
                method = success['method']
                method_counts[method] = method_counts.get(method, 0) + 1
            
            for method, count in method_counts.items():
                print(f"   {method}: {count} links verified")
            print()
        
        # Exit with error code if there are failures
        if self.results['failed']:
            print("🚨 SOME TESTS FAILED - Please review and fix broken links!")
            sys.exit(1)
        elif self.results['warnings']:
            print("⚠️  ALL TESTS PASSED WITH WARNINGS - Review recommended")
            sys.exit(0)
        else:
            print("🎉 ALL TESTS PASSED - No broken links found!")
            sys.exit(0)

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Exiles Installer Link Validation Test Suite")
        print("Usage: python test_links.py")
        print()
        print("Tests all URLs, GitHub repositories, and winget packages")
        print("defined in src/apps.json for accessibility and validity.")
        sys.exit(0)
    
    tester = LinkTester()
    tester.run_tests()

if __name__ == '__main__':
    main()