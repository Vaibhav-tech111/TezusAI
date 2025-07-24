# plugins/network_controller.py

from connectors.device_control import DeviceController

controller = DeviceController()

def wifi(state: str) -> str:
    """
    Turns WiFi on or off.
    state: 'on' or 'off'
    """
    if state not in ["on", "off"]:
        return "⚠️ Invalid WiFi state. Use 'on' or 'off'."
    return controller.toggle_wifi("enable" if state == "on" else "disable")

def bluetooth(state: str) -> str:
    """
    Turns Bluetooth on or off.
    state: 'on' or 'off'
    """
    if state not in ["on", "off"]:
        return "⚠️ Invalid Bluetooth state. Use 'on' or 'off'."
    return controller.toggle_bluetooth("enable" if state == "on" else "disable")
