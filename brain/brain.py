# brain/brain.py

from brain.parser import parse_intent
from brain.planner import generate_plan
from brain.fusion import fuse_results
from database.manager import DatabaseManager

class TezusBrain:
    def __init__(self):
        self.db = DatabaseManager()
        self.memory = self.load_memory()
        self.tools = self.load_tools()

    def load_memory(self):
        # Load user preferences, history, etc.
        return self.db.fetch_user_profile()

    def load_tools(self):
        # Register available plugins/tools
        return {
            "search": "web_search",
            "image": "image_generator",
            "voice": "stt_tts",
            "apps": "app_controller",
            "system": "system_control",
            "location": "location_manager",
            "network": "network_controller"
        }

    def plan(self, user_input: str):
        # Step 1: Parse intent
        intent_data = parse_intent(user_input)

        # Step 2: Generate roadmap
        task_plan = generate_plan(intent_data, self.memory)

        return task_plan

    def fuse(self, responses: list):
        # Combine multiple AI model outputs
        return fuse_results(responses)

    def update_memory(self, key, value):
        # Update memory in DB
        self.db.update_user_profile(key, value)
        self.memory[key] = value
