### PYTHON VERSION

I'm using python 3.12.8

<div id='howtostart'/>

## How to install Windows

```python
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
pip install -U https://github.com/iqoptionapi/iqoptionapi/archive/refs/heads/master.zip
```

## Run

Call run.bat

<div id='createexe'/>

## Create .exe

```python
pyinstaller --onefile --windowed prometey.py --onefile
```

open dist\prometey.exe

## Create installer .exe with Inno Setup

[Download](https://jrsoftware.org/isdl.php#stable)

Inno Setup script for installer

```pascal
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
```
