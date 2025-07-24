# plugins/input_controller.py

from inputs import get_gamepad

class InputController:
    def __init__(self):
        self.state = {}

    def update(self):
        """
        Polls input devices and updates internal state.
        """
        events = get_gamepad()
        for event in events:
            self.state[event.code] = event.state

    def get_button(self, button_name: str) -> bool:
        """
        Returns True if button is pressed.
        """
        return self.state.get(button_name, 0) == 1

    def get_axis(self, axis_name: str) -> float:
        """
        Returns normalized axis value.
        """
        raw = self.state.get(axis_name, 0)
        if "ABS_" in axis_name:
            return raw / 32767.0  # Normalize joystick axis
        return raw

    def get_state(self):
        """
        Returns full input state dictionary.
        """
        return self.state
