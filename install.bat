@echo off
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Locker_client" /t REG_SZ /d "%USERPROFILE%\Documents\locker_client-main\start.bat" /f
echo Программа добавлена в автозапуск.
pip install -r requirements.txt
echo Программа установила нужные библиотеки.
pause
