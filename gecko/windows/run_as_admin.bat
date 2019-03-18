SET FILE=%~dp0set_enviroment_varibel.ps1
echo %FILE%
Powershell.exe -ExecutionPolicy Unrestricted -File "%FILE%"
pause