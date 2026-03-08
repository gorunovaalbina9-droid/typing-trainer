; Inno Setup script для установки тренажёра слепой печати
; Требуется установленный Inno Setup: https://jrsoftware.org/isinfo.php

[Setup]
AppName=TypingTrainer
AppVersion=1.0
AppPublisher=Typing Trainer
DefaultDirName={autopf}\TypingTrainer
DefaultGroupName=TypingTrainer
DisableDirPage=no
OutputDir=Output
OutputBaseFilename=TypingTrainerSetup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "ru"; MessagesFile: "compiler:Languages\\Russian.isl"

[Files]
; Основной exe, собранный PyInstaller'ом
Source: "dist\\TypingTrainer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\TypingTrainer"; Filename: "{app}\\TypingTrainer.exe"
Name: "{userdesktop}\\TypingTrainer"; Filename: "{app}\\TypingTrainer.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительные значки:"; Flags: unchecked

[Run]
Filename: "{app}\\TypingTrainer.exe"; Description: "Запустить тренажёр слепой печати"; Flags: nowait postinstall skipifsilent

