[Setup]
AppName=ProjetoX
AppVersion=1.0
DefaultDirName={pf}\ProjetoX
DefaultGroupName=ProjetoX
OutputBaseFilename=ProjetoX_Installer
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes
WizardStyle=modern
AppPublisher=SeuNome
AppPublisherURL=https://exemplo.com
AppSupportURL=https://exemplo.com/suporte
AppUpdatesURL=https://exemplo.com/atualizacoes

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Files]
; EXE principal compilado pelo PyInstaller
Source: "dist\login.exe"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos JSON de dados
Source: "dados_projetos.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "dados_usuarios.json"; DestDir: "{app}"; Flags: ignoreversion

; Se quiser incluir também imagens ou PDFs gerados
; Source: "exemplos\*"; DestDir: "{app}\exemplos"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ProjetoX"; Filename: "{app}\login.exe"
Name: "{commondesktop}\ProjetoX"; Filename: "{app}\login.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Opções adicionais"; Flags: unchecked

[Run]
Filename: "{app}\login.exe"; Description: "Executar ProjetoX"; Flags: nowait postinstall skipifsilent
