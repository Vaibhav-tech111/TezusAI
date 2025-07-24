# brain/parser.py

import re
from typing import Dict

def parse_intent(user_input: str) -> Dict:
    """
    Parses user input and returns intent, entities, and confidence.
    """

    user_input = user_input.lower().strip()

    # Basic intent patterns
    patterns = {
        "open_app": r"(open|launch|start)\s+(\w+)",
        "close_app": r"(close|exit|stop)\s+(\w+)",
        "search_web": r"(search|look up|find)\s+(.*)",
        "generate_image": r"(generate|create|draw)\s+(image|picture|art)",
        "get_time": r"(what time|current time|tell me the time)",
        "get_date": r"(what date|today's date|current date)",
        "get_location": r"(where am i|my location|current location)",
        "control_wifi": r"(turn (on|off) wifi)",
        "control_bluetooth": r"(turn (on|off) bluetooth)",
        "system_action": r"(shutdown|restart|lock screen|power off)"
    }

    for intent, pattern in patterns.items():
        match = re.search(pattern, user_input)
        if match:
            return {
                "intent": intent,
                "entities": match.groups(),
                "confidence": 0.95
            }

    # Fallback
    return {
        "intent": "unknown",
        "entities": [],
        "confidence": 0.5
    }
