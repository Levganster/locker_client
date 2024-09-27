@echo off
python -m pip install -r requirements.txt
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Locker_client" /t REG_SZ /d "%USERPROFILE%\Documents\locker_client-main\start.bat" /f
pause
