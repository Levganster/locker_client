@echo off
chcp 65001
pip install -r requirements.txt
move C:\Users\kuzmi\Documents\locker_client-main\background.jpg C:\Windows\System32
echo Программа установила нужные библиотеки.
cls
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Locker_client" /t REG_SZ /d "%USERPROFILE%\Documents\locker_client-main\locker_client.exe" /f
echo Программа добавлена в автозапуск.
pause
