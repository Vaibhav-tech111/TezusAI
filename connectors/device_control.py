# connectors/device_control.py

import platform
import subprocess

class DeviceController:
    def __init__(self):
        self.os = platform.system()

    def toggle_wifi(self, state: str) -> str:
        if self.os == "Windows":
            cmd = f"netsh interface set interface name=\"Wi-Fi\" admin={state}"
        elif self.os == "Linux":
            cmd = f"nmcli radio wifi {'on' if state == 'enable' else 'off'}"
        else:
            return "Unsupported OS for WiFi control."

        return self.run_command(cmd)

    def toggle_bluetooth(self, state: str) -> str:
        if self.os == "Linux":
            cmd = f"rfkill {'unblock' if state == 'enable' else 'block'} bluetooth"
        elif self.os == "Windows":
            return "Bluetooth control not supported via CLI on Windows."
        else:
            return "Unsupported OS for Bluetooth control."

        return self.run_command(cmd)

    def adjust_volume(self, level: int) -> str:
        if self.os == "Linux":
            cmd = f"amixer set Master {level}%"
        elif self.os == "Windows":
            return "Volume control requires external library on Windows."
        else:
            return "Unsupported OS for volume control."

        return self.run_command(cmd)

    def run_command(self, cmd: str) -> str:
        try:
            subprocess.run(cmd, shell=True, check=True)
            return f"✅ Command executed: {cmd}"
        except subprocess.CalledProcessError as e:
            return f"❌ Command failed: {cmd}\nError: {e}"
