# plugins/system_control.py

import platform
import subprocess

def shutdown() -> str:
    os_type = platform.system()

    try:
        if os_type == "Windows":
            subprocess.call("shutdown /s /t 0", shell=True)
        elif os_type == "Linux":
            subprocess.call("shutdown now", shell=True)
        elif os_type == "Darwin":
            subprocess.call("sudo shutdown -h now", shell=True)
        else:
            return "Unsupported OS."

        return "🛑 System is shutting down."
    except Exception as e:
        return f"❌ Failed to shutdown: {e}"

def restart() -> str:
    os_type = platform.system()

    try:
        if os_type == "Windows":
            subprocess.call("shutdown /r /t 0", shell=True)
        elif os_type == "Linux":
            subprocess.call("reboot", shell=True)
        elif os_type == "Darwin":
            subprocess.call("sudo shutdown -r now", shell=True)
        else:
            return "Unsupported OS."

        return "🔁 System is restarting."
    except Exception as e:
        return f"❌ Failed to restart: {e}"

def lock_screen() -> str:
    os_type = platform.system()

    try:
        if os_type == "Windows":
            subprocess.call("rundll32.exe user32.dll,LockWorkStation", shell=True)
        elif os_type == "Linux":
            subprocess.call("gnome-screensaver-command -l", shell=True)
        elif os_type == "Darwin":
            subprocess.call("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend", shell=True)
        else:
            return "Unsupported OS."

        return "🔒 Screen locked."
    except Exception as e:
        return f"❌ Failed to lock screen: {e}"
