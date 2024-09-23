@echo off
:: Находим путь к pythonw.exe и сохраняем в переменную
for /f "usebackq" %%i in (`where pythonw`) do set "pythonw_path=%%i"

:: Проверяем, нашли ли путь
if not defined pythonw_path (
    echo Не удалось найти pythonw.exe.
    pause
    exit /b
)
start "" "%pythonw_path%" "%USERPROFILE%\Documents\locker_client-main\tests\customtheme.py"
exit