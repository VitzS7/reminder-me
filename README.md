# 🔔 Reminder Me

A lightweight Windows desktop reminder app with native toast notifications, multiple repeat modes, and multi-language support.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python) ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows) ![License](https://img.shields.io/badge/License-MIT-green) ![Version](https://img.shields.io/badge/Version-1.0.0-informational)

---

## Download

Go to the [Releases](https://github.com/VitzS7/reminder-me/releases) page and download **ReminderMe.exe**. No Python required.

> Windows Defender may flag the `.exe` as a false positive — this is common with PyInstaller apps. Whitelist it or build from source.

---

## Features

- 🔔 Native Windows toast notifications with app icon in the header
- 🔁 Seven repeat modes: Once, Every hour, Daily, Every X minutes, Weekly, Monthly, Specific date
- 🌍 Five languages: English, Português (Brasil), Español, Русский, 中文
- 🌙 / ☀️ Follows system light/dark theme automatically
- 😀 Emoji picker with category tabs
- 🕐 Visual time picker — click to type or use arrow buttons
- 🖥️ Minimizes to system tray, keeps running in background
- 🗑️ One-time reminders deleted automatically after they fire
- 💾 Data stored locally next to the app

---

## Running from Source

**Requirements:** Python 3.10+, Windows 10/11

```bash
git clone https://github.com/VitzS7/reminder-me.git
cd reminder-me
pip install customtkinter pillow pystray winotify
python reminder_me.py
```

> Falls back to `plyer` if `winotify` is unavailable: `pip install plyer`

---

## Building the .exe

```bash
# Option A — one-click
build.bat

# Option B — manual
pip install pyinstaller
pyinstaller reminder_me.spec
# output: dist\ReminderMe.exe
```

Make sure `icon.ico` is in the project folder before building.

---

## Repeat Modes

| Mode | Behaviour |
|---|---|
| Once | Fires once, then deleted |
| Every hour | Fires every hour from creation |
| Daily | Every day at the set time |
| Every X minutes | Every X minutes from creation |
| Weekly | Every week on the chosen day |
| Monthly | Every month on the chosen day |
| Specific date | Fires once on a date/time, then deleted |

---

## Project Structure

```
reminder-me/
├── reminder_me.py       # Application
├── reminder_me.spec     # PyInstaller config
├── build.bat            # One-click build (Windows)
├── icon.ico             # App icon — window / taskbar / exe (auto-generated)
├── icon.png             # App icon — toast notifications  (auto-generated)
├── reminders.json       # Saved reminders (auto-created)
├── settings.json        # Preferences    (auto-created)
├── CHANGELOG.md
└── README.md
```

All runtime files are created automatically on first launch and regenerated if deleted.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

*Made by [VitzS7](https://github.com/VitzS7) · Instagram [@vitin_xzx](https://instagram.com/vitin_xzx)*
