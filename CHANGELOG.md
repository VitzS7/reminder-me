# Changelog

## [v1.0.0] — 2026-02-28

Initial release of **Reminder Me**.

### Features
- Native Windows toast notifications with app icon (winotify / plyer fallback)
- Seven repeat modes: Once, Every hour, Daily, Every X minutes, Weekly, Monthly, Specific date
- Multi-language: English, Português (Brasil), Español, Русский, 中文
- Follows system light/dark theme automatically
- Visual time picker — click the number to type or use the arrows
- Emoji picker with six category tabs
- Two-column layout with scrollable reminder cards
- Minimizes to system tray — click tray icon to restore
- One-time reminders deleted automatically after firing
- App icon registered in Windows registry for correct notification header icon
- All data files stored next to the executable (`reminders.json`, `settings.json`, `icon.ico`, `icon.png`)
- PyInstaller `.spec` and `build.bat` for one-click Windows `.exe` build
