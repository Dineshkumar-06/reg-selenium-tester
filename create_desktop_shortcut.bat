@echo off
setlocal
set "APPDIR=%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$lnk = $ws.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Reg Selenium Tester.lnk'));" ^
  "$lnk.TargetPath = '%APPDIR%start.bat';" ^
  "$lnk.WorkingDirectory = '%APPDIR%';" ^
  "$lnk.IconLocation = '%APPDIR%dashboard\static\app_icon.ico';" ^
  "$lnk.Description = 'Launch Reg Selenium Tester Dashboard';" ^
  "$lnk.Save()"

echo Desktop shortcut created: "Reg Selenium Tester"
pause
