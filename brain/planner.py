# brain/planner.py

from typing import Dict, List

def generate_plan(intent_data: Dict, memory: Dict) -> List[Dict]:
    """
    Converts parsed intent into a structured task plan.
    Each step is a dictionary with plugin, action, and parameters.
    """

    intent = intent_data.get("intent")
    entities = intent_data.get("entities", [])

    if not intent or not isinstance(entities, list):
        return [] #Handle missing or invalid input

    plan = []
    intent_map = {
        "open_app": {"plugin": "app_controller", "action": "open", "params": lambda entities: {"app": entities[-1]}},
        "close_app": {"plugin": "app_controller", "action": "close", "params": lambda entities: {"app": entities[-1]}},
        "search_web": {"plugin": "web_search", "action": "search", "params": lambda entities: {"query": entities[-1]}},
        "generate_image": {"plugin": "image_generator", "action": "generate", "params": lambda entities: {"prompt": " ".join(entities)}},
        "get_time": {"plugin": "system_info", "action": "get_time", "params": lambda entities: {}},
        "get_date": {"plugin": "system_info", "action": "get_date", "params": lambda entities: {}},
    }

    intent_plan = intent_map.get(intent)
    if intent_plan:
        try:
            plan.append({
                "plugin": intent_plan["plugin"],
                "action": intent_plan["action"],
                "params": intent_plan["params"](entities)
            })
        except IndexError:
            return [] #Handle cases where entities is empty for intents requiring them.

    return plan