# GTA V — Solo Public Lobby Tool

A professional Windows 11 desktop GUI that puts you into a **solo public session** in GTA Online with a single click — no modding, no memory injection, no sketchy software.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![GTA V](https://img.shields.io/badge/Game-GTA%20V%20Online-black?style=flat-square)

---

## What It Does

GTA Online uses peer-to-peer sessions. By briefly suspending the `GTA5.exe` process, every other player's connection times out and they are dropped from the session. When the process resumes, you remain in a **public lobby — completely alone**.

This means:
- ✅ CEO / VIP work and businesses continue to function
- ✅ Bunker, Nightclub, and cargo sales work normally
- ✅ No griefers, no modders, no interference
- ✅ Full money and XP earning, same as any public session

---

## Preview

| Status | In Progress | Done |
|--------|-------------|------|
| ![ready](https://img.shields.io/badge/GTA5.exe-Detected-brightgreen?style=flat-square) | Countdown progress bar | Solo session active |

> The GUI features a live process detector, adjustable suspend timer, animated progress bar, and a timestamped event log — all in a clean Windows 11 dark theme.

---

## Requirements

| Requirement | Details |
|-------------|---------|
| OS | Windows 10 or Windows 11 |
| Python | 3.9 or newer |
| Packages | `customtkinter >= 5.2.0`, `psutil >= 5.9.0` |
| Permissions | Administrator (required to suspend processes) |
| Game | GTA V loaded into an Online public session |

---

## Quick Start

**1. Install Python 3.9+**
Download from [python.org](https://www.python.org/downloads/) — check **"Add Python to PATH"** during setup.

**2. Clone or download this repository**
```bash
git clone https://github.com/YOUR-USERNAME/gtav-solo-lobby-tool.git
cd gtav-solo-lobby-tool
```

**3. Double-click `launch.bat`**

That's it. The batch file will:
- Verify Python is installed
- Auto-install `customtkinter` and `psutil`
- Launch the tool with Administrator privileges

**4. Load into a GTA Online public session, then click "Launch Solo Session"**

---

## How It Works

```
1. Tool detects GTA5.exe via psutil
2. Calls NtSuspendProcess (via psutil.suspend())
3. Waits 7–10 seconds (adjustable via slider)
4. Calls NtResumeProcess (via psutil.resume())
5. All other players have timed out — you remain in the session alone
```

This is the same technique used manually via Windows Resource Monitor / Task Manager, fully automated with a clean GUI wrapper.

---

## GUI Overview

| Element | Description |
|---------|-------------|
| **Process Status** | Live green/red indicator — polls GTA5.exe every 2 seconds |
| **Suspend Duration** | Slider from 5–15 seconds (default: 8 s) |
| **Progress Bar** | Animated countdown during the suspend phase |
| **Launch Button** | Disabled until GTA5.exe is detected; shows live countdown |
| **Event Log** | Timestamped record of every action with a Clear button |

---

## Files

```
gtav-solo-lobby-tool/
├── solo_lobby_tool.py   # Main GUI application
├── launch.bat           # One-click installer and launcher
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
├── README.md            # This file
└── README.txt           # Offline plain-text documentation
```

---

## Troubleshooting

**"Access Denied" error**
> Right-click `launch.bat` → **Run as administrator**, or approve the UAC prompt when it appears.

**Green dot never appears**
> Make sure GTA V is fully loaded into an **Online** session (not Story Mode). Confirm the process shows as `GTA5.exe` in Task Manager.

**Players are not kicked**
> Increase the slider to **10–12 seconds** and try again.

**You get kicked from the session**
> The suspend time is too long. Reduce the slider to **7–8 seconds**.

**Python not found**
> Reinstall Python and make sure **"Add Python to PATH"** is checked during setup. Then restart your terminal or PC.

---

## Disclaimer

This tool does **not**:
- Inject code into GTA V
- Modify game memory or files
- Interact with Rockstar's servers
- Use or include any mod menus

It only suspends and resumes your own Windows process using a standard OS API — the same action you would perform manually in Task Manager. Use responsibly and at your own discretion.

---

## License

This project is licensed under the [MIT License](LICENSE).
Free to use, modify, and distribute with attribution.

---

## Contributing

Pull requests are welcome. If you have suggestions for new features (e.g. auto-detect session load, system tray mode, hotkey support), feel free to open an issue.
