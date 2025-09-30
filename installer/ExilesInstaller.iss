; ? Project: Exiles Installer
; ? File: ExilesInstaller.iss
; ? Directory: installer/
; ? Description: Inno Setup script to package the onedir build, add shortcuts, and uninstall.
; ? Created by: Watty
; ? Created on: 2025-09-30
; ? Last modified by: Watty
; ? Last modified on: 2025-09-30

#define MyAppName "Exiles Installer"
#define MyAppVersion GetEnv("EXILES_INSTALLER_VERSION")
#if MyAppVersion == ""
  #define MyAppVersion "1.0.0"
#endif
#define MyAppPublisher "The Exiles"
#define MyAppURL "https://theexiles.gg"
#define MyAppExeName "ExilesInstaller.exe"

[Setup]
AppId={{D2B1A4E8-0B51-4A86-9E5C-4C9E04B7A2C1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableDirPage=no
DisableProgramGroupPage=no
OutputBaseFilename=ExilesInstaller-{#MyAppVersion}-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
; SetupIconFile=icons\exiles.ico   ; comment out until you add installer/icons/exiles.ico
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "..\dist\ExilesInstaller\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\logs"
