# connectors/device_control.py

import platform
import subprocess
import logging
import re
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DeviceController:
    def __init__(self):
        self.os = platform.system()

    def toggle_wifi(self, state: str) -> str:
        if state.lower() not in ["enable", "disable"]:
            return "Invalid state. Use 'enable' or 'disable'."

        if self.os == "Windows":
            try:
                interfaces = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')
                match = re.search(r'Name\s*:\s*(\S+)', interfaces)
                if match:
                    interface_name = match.group(1)
                    cmd = ['netsh', 'interface', 'set', 'interface', 'name="' + interface_name + '"', 'admin=' + state]
                else:
                    return "Could not determine Wi-Fi interface name."
                subprocess.check_call(cmd)
                return "Wi-Fi toggled successfully."
            except subprocess.CalledProcessError as e:
                return f"Error toggling Wi-Fi: {e}"
        elif self.os == "Linux":
            cmd = ['nmcli', 'radio', 'wifi', 'on' if state == 'enable' else 'off']
            try:
                subprocess.check_call(cmd)
                return "Wi-Fi toggled successfully."
            except subprocess.CalledProcessError as e:
                return f"Error toggling Wi-Fi: {e}"
        elif self.os == "Darwin": # macOS support
            cmd = ['networksetup', '-setairportpower', 'en0', 'on' if state == 'enable' else 'off'] # Assumes en0, adjust if needed.
            try:
                subprocess.check_call(cmd)
                return "Wi-Fi toggled successfully."
            except subprocess.CalledProcessError as e:
                return f"Error toggling Wi-Fi: {e}"
        else:
            return "Unsupported OS for WiFi control."

    def toggle_bluetooth(self, state: str) -> str:
        if state.lower() not in ["enable", "disable"]:
            return "Invalid state. Use 'enable' or 'disable'."

        if self.os == "Linux":
            cmd = ['rfkill', 'unblock' if state == 'enable' else 'block', 'bluetooth']
            try:
                subprocess.check_call(cmd)
                return "Bluetooth toggled successfully."
            except subprocess.CalledProcessError as e:
                return f"Error toggling Bluetooth: {e}"
        elif self.os == "Darwin": # macOS support
            cmd = ['/usr/bin/osascript', '-e', 'tell application "System Events" to set the value of the checkbox "Bluetooth" of the Bluetooth pane of the system preferences to ' + ('true' if state == 'enable' else 'false')]
            try:
                subprocess.check_call(cmd)
                return "Bluetooth toggled successfully."
            except subprocess.CalledProcessError as e:
                return f"Error toggling Bluetooth: {e}"
        elif self.os == "Windows":
            logging.warning("Bluetooth control on Windows requires an external library.  Consider using pywin32.")
            return "Bluetooth control not directly supported on Windows."
        else:
            return "Unsupported OS for Bluetooth control."


    def adjust_volume(self, level: int) -> str:
        if not 0 <= level <= 100:
            return "Volume level must be between 0 and 100."

        if self.os == "Linux":
            cmd = ['amixer', 'set', 'Master', f'{level}%']
            try:
                subprocess.check_call(cmd)
                return "Volume adjusted successfully."
            except subprocess.CalledProcessError as e:
                return f"Error adjusting volume: {e}"
        elif self.os == "Darwin": # macOS support
            cmd = ['osascript', '-e', f'set volume output volume {level}']
            try:
                subprocess.check_call(cmd)
                return "Volume adjusted successfully."
            except subprocess.CalledProcessError as e:
                return f"Error adjusting volume: {e}"
        elif self.os == "Windows":
            logging.warning("Volume control on Windows requires an external library. Consider using pycaw.")
            return "Volume control not directly supported on Windows."
        else:
            return "Unsupported OS for volume control."