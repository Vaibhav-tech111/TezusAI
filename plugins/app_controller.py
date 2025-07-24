# plugins/app_controller.py

import platform
import subprocess

def open(app: str) -> str:
    os_type = platform.system()

    try:
        if os_type == "Windows":
            subprocess.Popen(f"start {app}", shell=True)
        elif os_type == "Linux":
            subprocess.Popen([app])
        elif os_type == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app])
        else:
            return "Unsupported OS."

        return f"✅ Opened app: {app}"
    except Exception as e:
        return f"❌ Failed to open app: {e}"

def close(app: str) -> str:
    os_type = platform.system()

    try:
        if os_type == "Windows":
            subprocess.call(f"taskkill /IM {app}.exe /F", shell=True)
        elif os_type == "Linux":
            subprocess.call(["pkill", app])
        elif os_type == "Darwin":
            subprocess.call(["killall", app])
        else:
            return "Unsupported OS."

        return f"✅ Closed app: {app}"
    except Exception as e:
        return f"❌ Failed to close app: {e}"
