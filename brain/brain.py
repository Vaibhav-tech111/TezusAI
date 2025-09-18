# brain/brain.py

from brain.parser import parse_intent
from brain.planner import generate_plan
from brain.fusion import fuse_results
from database.manager import DatabaseManager
from typing import Dict, List, Any
import logging
import importlib

logging.basicConfig(level=logging.INFO) # Configure logging

class TezusBrain:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.memory = self.load_memory()
        self.tools = self.load_tools()

    def load_memory(self) -> Dict[str, Any]:
        try:
            return self.db.fetch_user_profile()
        except Exception as e:
            logging.error(f"Error loading memory: {e}")
            return {} # Return empty dict on failure

    def load_tools(self) -> Dict[str, str]:
        try:
            # Load tool mappings from a config file or database
            # For now, using a sample configuration
            return {
                "search": "web_search",
                "image": "image_generator",
                "voice": "stt_tts",
                "apps": "app_controller",
                "system": "system_control",
                "location": "location_manager",
                "network": "network_controller"
            }
        except Exception as e:
            logging.error(f"Error loading tools: {e}")
            return {} #Return empty dict on failure

    def plan(self, user_input: str) -> List[Dict[str, Any]]:
        try:
            intent_data = parse_intent(user_input)
            task_plan = generate_plan(intent_data, self.memory)
            executed_plan = self._execute_plan(task_plan)
            return executed_plan
        except Exception as e:
            logging.error(f"Error during planning: {e}")
            return []

    def _execute_plan(self, task_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        executed_tasks = []
        for task in task_plan:
            tool_name = task.get("tool")
            tool_module = self.tools.get(tool_name)
            if tool_module:
                try:
                    module = importlib.import_module(f"tools.{tool_module}")
                    tool = getattr(module, tool_module)
                    result = tool(**task.get("params", {}))
                    task["result"] = result
                    executed_tasks.append(task)
                except ImportError as e:
                    logging.error(f"Error importing tool {tool_module}: {e}")
                    task["error"] = f"ImportError: {e}"
                    executed_tasks.append(task)
                except Exception as e:
                    logging.error(f"Error executing tool {tool_module}: {e}")
                    task["error"] = str(e)
                    executed_tasks.append(task)
            else:
                logging.warning(f"Tool '{tool_name}' not found.")
        return executed_tasks


    def fuse(self, responses: List[Any]) -> Any:
        if not isinstance(responses, list):
            logging.error("Invalid input to fuse: responses must be a list.")
            return None
        if not all(isinstance(r, dict) and "result" in r for r in responses):
            logging.warning("Invalid response format in fuse.  Expecting a list of dictionaries with a 'result' key.")
        return fuse_results(responses)

    def update_memory(self, key: str, value: Any):
        try:
            self.db.update_user_profile(key, value)
            self.memory[key] = value # Update local copy after successful DB update
        except Exception as e:
            logging.error(f"Error updating memory: {e}")