# Changelog

## [v1.0.1] — 2026-02-28

### Changed
- **Data subfolder** — all generated files (`icon.ico`, `icon.png`, `reminders.json`, `settings.json`) are now stored in a `reminder-me/` subfolder next to the executable.
- **Icon quality** — the bell icon is now rendered at 4× resolution (1024 px) and downscaled with LANCZOS anti-aliasing, eliminating the jagged/pixelated edges seen in v1.0.0. Redesigned with a smooth scanline bell body, radial gradient background, specular highlight on the dome, and a red notification badge with depth shadow.

---

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
- PyInstaller `.spec` and `build.bat` for one-click Windows `.exe` build
