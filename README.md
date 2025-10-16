# Windows 11 Control Panel (Python GUI)

A modern Windows 11–inspired Control Panel built with Python and CustomTkinter, featuring multiple user roles, real system volume control, and admin tools.

✨ Features
🧑‍💼 Multi-User System

👑 Admin – Full access (Settings + Admin Panel + System Tools)

👤 User – Limited access (Home + Settings)

🧳 Guest – Basic access (Home only)

⚙️ Control Panel Functions

🎚️ System Volume Control

Real-time control of Windows system volume

Live percentage display

Mute / Unmute button

🎨 Theme Selector

Switch between System, Dark, and Light modes instantly

🛠️ Admin Tools

Open Task Manager, CMD, File Explorer

Restart or Shutdown the PC directly

(Requires Admin role)

Design

Clean, rounded Windows 11–style interface

Sidebar navigation with icons

Responsive, multi-page layout

Built entirely in CustomTkinter (no web or external GUI frameworks)

🧰 Installation
1️⃣ Clone or Download
```bash
git clone https://github.com/diecrewls22-dev/win11-control-panel.git
cd win11-control-panel
```

2️⃣ Install Dependencies

Make sure you have Python 3.9+ installed, then run:
```bash
pip install customtkinter pycaw comtypes
```

3️⃣ Run the Program
```cmd
python gui.py
```

🔐 Login Credentials
Role	    Username	Password	Access
👑 Admin	admin	    admin123	Full access
👤 User	    user	    user123	    Limited access
🧳 Guest	guest	    guest	    Home only

🧩 Tech Stack

- Python 3.9+

- CustomTkinter – modern UI components

- Pycaw – Windows Core Audio API wrapper

- Tkinter – core GUI engine

- comtypes – for COM interaction with Windows audio

📂 Project Structure
win11-control-panel/
├── control_panel.py   # Main application
├── README.md          # Documentation
└── requirements.txt   # (optional) Dependency list

⚠️ Notes

- Works only on Windows (uses Windows audio APIs).

- Requires permission to access system audio and system commands.

- Do not run admin tools (restart/shutdown) unless you intend to!

!

🚀 Planned Additions

✅ Custom user creation & password change
✅ Live system info (CPU, RAM, network)
✅ Better Windows 11–like theme (with Fluent Design)

🧑‍💻 Author

diecrewls22
Made with ❤️ in Visual Studio Code
For learning, fun, and automation projects.