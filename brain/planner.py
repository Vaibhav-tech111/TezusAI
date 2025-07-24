# brain/planner.py

from typing import Dict, List

def generate_plan(intent_data: Dict, memory: Dict) -> List[Dict]:
    """
    Converts parsed intent into a structured task plan.
    Each step is a dictionary with plugin, action, and parameters.
    """

    intent = intent_data.get("intent")
    entities = intent_data.get("entities", [])

    plan = []

    if intent == "open_app":
        app_name = entities[-1]
        plan.append({
            "plugin": "app_controller",
            "action": "open",
            "params": {"app": app_name}
        })

    elif intent == "close_app":
        app_name = entities[-1]
        plan.append({
            "plugin": "app_controller",
            "action": "close",
            "params": {"app": app_name}
        })

    elif intent == "search_web":
        query = entities[-1]
        plan.append({
            "plugin": "web_search",
            "action": "search",
            "params": {"query": query}
        })

    elif intent == "generate_image":
        prompt = " ".join(entities)
        plan.append({
            "plugin": "image_generator",
            "action": "generate",
            "params": {"prompt": prompt}
        })

    elif intent == "get_time":
        plan.append({
            "plugin": "system_info",
            "action": "get_time",
            "params": {}
        })

    elif intent == "get_date":
        plan.append({
            "plugin": "system_info",
            "action": "get_date",
            "
