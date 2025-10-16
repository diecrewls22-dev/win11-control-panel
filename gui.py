import customtkinter as ctk
from tkinter import messagebox
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import os
import subprocess

# ─────────────────────────────
# System Volume Control (pycaw)
# ─────────────────────────────
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def get_system_volume():
    """Return system volume as 0–100 (0 = mute, 100 = max)."""
    return int(volume.GetMasterVolumeLevelScalar() * 100)

def set_system_volume(level):
    """Set system volume 0–100 (0 = mute, 100 = max)."""
    level = max(0, min(100, level))
    volume.SetMasterVolumeLevelScalar(level / 100, None)

def toggle_mute():
    """Toggle mute state."""
    current = volume.GetMute()
    volume.SetMute(not current, None)
    return not current  # Return new mute state

def is_muted():
    return bool(volume.GetMute())

# ─────────────────────────────
# Account Data (simple example)
# ─────────────────────────────
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "user123", "role": "User"},
    "guest": {"password": "guest", "role": "Guest"}
}

current_user = None

# ─────────────────────────────
# App setup
# ─────────────────────────────
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Windows 11 Control Panel")
app.geometry("850x520")

# ─────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────
login_frame = ctk.CTkFrame(app)
login_frame.pack(fill="both", expand=True)

ctk.CTkLabel(login_frame, text="🔐 Login to Control Panel",
             font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(100, 10))
username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", width=220)
username_entry.pack(pady=5)
password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="•", width=220)
password_entry.pack(pady=5)

def login():
    global current_user
    username = username_entry.get().lower()
    password = password_entry.get()
    if username in users and users[username]["password"] == password:
        current_user = users[username]
        messagebox.showinfo("Login Successful", f"Welcome, {username.title()}!")
        login_frame.pack_forget()
        open_main_panel(current_user["role"])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

ctk.CTkButton(login_frame, text="Login", command=login, width=220).pack(pady=10)

# ─────────────────────────────
# MAIN PANEL (Created after login)
# ─────────────────────────────
def open_main_panel(role):
    nav_frame = ctk.CTkFrame(app, width=200, corner_radius=0)
    nav_frame.pack(side="left", fill="y")

    pages = {}

    def show_page(name: str):
        for frame in pages.values():
            frame.pack_forget()
        pages[name].pack(fill="both", expand=True, padx=20, pady=20)

    # Sidebar
    ctk.CTkLabel(nav_frame, text=f"⚙️ {role} Panel", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20,40))
    ctk.CTkButton(nav_frame, text="🏠 Home", width=180, command=lambda: show_page("home")).pack(pady=5)
    if role in ["Admin", "User"]:
        ctk.CTkButton(nav_frame, text="⚙️ Settings", width=180, command=lambda: show_page("settings")).pack(pady=5)
    if role == "Admin":
        ctk.CTkButton(nav_frame, text="🛡️ Admin", width=180, command=lambda: show_page("admin")).pack(pady=5)
    ctk.CTkButton(nav_frame, text="🔒 Logout", width=180, fg_color="#d9534f", hover_color="#c9302c",
                  command=lambda: logout(nav_frame, pages)).pack(side="bottom", pady=20)

    # ───── HOME PAGE ─────
    home = ctk.CTkFrame(app)
    ctk.CTkLabel(home, text=f"Welcome, {role}!",
                 font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)
    ctk.CTkLabel(home, text="Use the sidebar to navigate.", justify="center").pack()
    pages["home"] = home

    # ───── SETTINGS PAGE ─────
    if role in ["Admin", "User"]:
        settings = ctk.CTkFrame(app)
        ctk.CTkLabel(settings, text="Settings", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        # Appearance theme
        theme_var = ctk.StringVar(value="system")

        def apply_theme():
            ctk.set_appearance_mode(theme_var.get())
            messagebox.showinfo("Theme Updated", f"Theme changed to {theme_var.get().title()} mode!")

        ctk.CTkLabel(settings, text="Appearance Mode:").pack(pady=(10,0))
        for theme in ["system","dark","light"]:
            ctk.CTkRadioButton(settings, text=theme.title(), variable=theme_var, value=theme).pack(anchor="w", padx=60)
        ctk.CTkButton(settings, text="Apply", command=apply_theme).pack(pady=10)

        # Volume control
        volume_var = ctk.DoubleVar(value=get_system_volume())
        muted = ctk.BooleanVar(value=is_muted())

        def update_volume(value):
            set_system_volume(float(value))
            volume_label.configure(text=f"Volume: {int(float(value))}%")

        def toggle_mute_button():
            new_state = toggle_mute()
            muted.set(new_state)
            if new_state:
                mute_button.configure(text="🔇 Unmute")
            else:
                mute_button.configure(text="🔊 Mute")

        ctk.CTkLabel(settings, text="System Volume:").pack(pady=(20,0))
        volume_slider = ctk.CTkSlider(settings, variable=volume_var, from_=0, to=100, command=update_volume)
        volume_slider.pack(padx=60)
        volume_label = ctk.CTkLabel(settings, text=f"Volume: {get_system_volume()}%")
        volume_label.pack(pady=(5,0))
        mute_button = ctk.CTkButton(settings,
                                    text="🔇 Unmute" if muted.get() else "🔊 Mute",
                                    command=toggle_mute_button)
        mute_button.pack(pady=10)

        pages["settings"] = settings

    # ───── ADMIN PAGE ─────
    if role == "Admin":
        admin = ctk.CTkFrame(app)
        ctk.CTkLabel(admin, text="Admin Panel", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        def open_taskmgr(): os.system("start taskmgr")
        def open_cmd(): subprocess.Popen("cmd", creationflags=subprocess.CREATE_NEW_CONSOLE)
        def restart_pc(): os.system("shutdown /r /t 0")
        def shutdown_pc(): os.system("shutdown /s /t 0")
        def open_explorer(): os.system("start explorer")

        ctk.CTkLabel(admin, text="Admin Tools", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        ctk.CTkButton(admin, text="Open Task Manager", command=open_taskmgr, width=180).pack(pady=5)
        ctk.CTkButton(admin, text="Open Command Prompt", command=open_cmd, width=180).pack(pady=5)
        ctk.CTkButton(admin, text="Open File Explorer", command=open_explorer, width=180).pack(pady=5)
        ctk.CTkButton(admin, text="Restart PC", command=restart_pc, fg_color="#f0ad4e").pack(pady=5)
        ctk.CTkButton(admin, text="Shutdown PC", command=shutdown_pc, fg_color="#d9534f").pack(pady=5)
        pages["admin"] = admin

    # Default page
    show_page("home")

def logout(nav_frame, pages):
    """Log out and return to login screen"""
    for frame in pages.values():
        frame.pack_forget()
    nav_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")
    messagebox.showinfo("Logout", "You have been logged out.")

app.mainloop()
