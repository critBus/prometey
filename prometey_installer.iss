[Setup]
AppName=Prometey
AppVersion=1.0
DefaultDirName={autopf}\Prometey
DefaultGroupName=Prometey
OutputDir=.
OutputBaseFilename=PrometeySetup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\prometey.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Prometey"; Filename: "{app}\prometey.exe"
Name: "{group}\Desinstalar Prometey"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\prometey.exe"; Description: "Iniciar Prometey"; Flags: nowait postinstall skipifsilent