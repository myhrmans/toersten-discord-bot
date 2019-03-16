set mypath=%~dp0
echo %mypath%
setx /M Path "%path%; %~dp0"
regedit.exe
pause