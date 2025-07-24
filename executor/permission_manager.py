# executor/permission_manager.py

class PermissionManager:
    def __init__(self):
        # Default permission rules (can be loaded from config)
        self.rules = {
            "system_control": "ask",     # shutdown, restart, lock
            "location_manager": "ask",   # access location
            "network_controller": "auto",# wifi/bluetooth toggle
            "app_controller": "auto",    # open/close apps
            "image_generator": "auto",   # generate image
            "ai_models": "auto",         # chat/fusion
        }

        # User preferences (can be loaded from DB)
        self.user_preferences = {}

    def is_allowed(self, plugin_name: str, action: str) -> bool:
        """
        Checks if the plugin/action is allowed based on rules and preferences.
        """

        rule = self.rules.get(plugin_name, "ask")
        user_pref = self.user_preferences.get(f"{plugin_name}.{action}")

        # If user has explicitly allowed/denied
        if user_pref == "allow":
            return True
        elif user_pref == "deny":
            return False

        # If rule is auto, allow
        if rule == "auto":
            return True

        # If rule is ask, prompt user
        return self.ask_user(plugin_name, action)

    def ask_user(self, plugin_name: str, action: str) -> bool:
        """
        Simulates asking user for permission.
        Replace with UI prompt or voice confirmation.
        """
        print(f"🔐 Permission required: {plugin_name}.{action}")
        response = input("Allow this action? (yes/no): ").strip().lower()
        return response == "yes"

    def set_user_preference(self, plugin_action: str, decision: str):
        """
        Stores user decision for future reference.
        """
        self.user_preferences[plugin_action] = decision
