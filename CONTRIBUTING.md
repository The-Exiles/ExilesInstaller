# Contributing to ExilesInstaller

Thanks for your interest in contributing! This document explains how to get set up, propose changes, and help us keep quality high.

Please read and follow our Code of Conduct: CODE_OF_CONDUCT.md

## Ways to contribute
- Report bugs using the GitHub issue templates
- Suggest features via the feature request template
- Improve docs (README, docs/, templates)
- Triage issues (add details, minimal reproductions)
- Submit pull requests for bugs or features

## Development setup
Prerequisites:
- Windows 10/11 (the app targets Windows)
- Python 3.11+ and Git

Setup steps:
1. Fork and clone the repository
2. Create a virtual environment
   - PowerShell
     - `python -m venv .venv`
     - `./.venv/Scripts/Activate.ps1`
3. Install dependencies
   - `pip install -r requirements.txt`
   - For running tests: `pip install pytest`
4. Run tests locally
   - `pytest -q`

Tips:
- If tests depend on network access or Windows features, run them on Windows.
- Artifacts and logs may be generated in `artifacts/` and can help diagnose issues.

## Coding guidelines
- Keep changes focused and easy to review.
- Use clear names, small functions, and add docstrings/comments where helpful.
- Prefer readability over cleverness.
- Update or add tests where it makes sense.

### Commit messages
- Use imperative tense: "Fix bug" not "Fixed"
- Reference issues: `Fixes #123` or `Closes #123`

### Pull requests
- Create a feature branch from `main`
- Fill in the PR template checklist
- Include steps for reviewers to test
- Make sure CI (if any) is passing

## Building installers (optional)
- Portable build: check `build_release.py` and `ExilesInstaller.spec`
- Inno Setup: see `installer/*.iss` (installer output goes to `installer/Output/`)

## Reporting security issues
Please do not open a public issue for security vulnerabilities. See SECURITY.md for private reporting instructions.
