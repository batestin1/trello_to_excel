@echo off
set OS=Windows_NT

if "%OS%" == "Windows_NT" (
echo Checking if Chocolatey is installed...
choco --version >nul 2>&1

if errorlevel 1 (
echo Installing Chocolatey...
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
)

echo Installing Python...
choco install python
echo Installing o pip...
choco install python-pip
echo Installing requeriments...
pip install -r pips/requeriments.txt
echo Running the project...
python scripts/main.py
) else (
echo Running the shell script...
bash
sh exec/others/init.sh
)