@echo off
echo ============================================
echo  Reminder Me - Build Script
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause & exit /b 1
)

echo Installing dependencies...
pip install customtkinter pillow pystray winotify pyinstaller

echo.
echo Building ReminderMe.exe...
pyinstaller reminder_me.spec

echo.
if exist "dist\ReminderMe.exe" (
    echo Build successful! dist\ReminderMe.exe
) else (
    echo Build failed. Check errors above.
)
pause
