# brain/brain.py

from brain.parser import parse_intent
from brain.planner import generate_plan
from brain.fusion import fuse_results
from database.manager import DatabaseManager
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.ERROR) # Configure logging

class TezusBrain:
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager or DatabaseManager()
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
            # Execute the plan here
            executed_plan = self._execute_plan(task_plan)
            return executed_plan
        except Exception as e:
            logging.error(f"Error during planning: {e}")
            return []

    def _execute_plan(self, task_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        executed_tasks = []
        for task in task_plan:
            tool_name = task.get("tool")
            tool = self.tools.get(tool_name)
            if tool:
                try:
                    # Execute the tool (replace with actual tool execution)
                    result = self._execute_tool(tool, task.get("params", {}))
                    task["result"] = result
                    executed_tasks.append(task)
                except Exception as e:
                    logging.error(f"Error executing tool {tool}: {e}")
                    task["error"] = str(e)
                    executed_tasks.append(task)
            else:
                logging.warning(f"Tool '{tool_name}' not found.")
        return executed_tasks

    def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        # Placeholder for tool execution - replace with actual implementation
        # This would involve importing and calling the specific tool module
        # based on tool_name and passing params.
        # Example:
        # from tools import web_search
        # return web_search(**params)
        return f"Result from tool: {tool_name} with params: {params}"


    def fuse(self, responses: List[Any]) -> Any:
        if not isinstance(responses, list):
            logging.error("Invalid input to fuse: responses must be a list.")
            return None
        return fuse_results(responses)

    def update_memory(self, key: str, value: Any):
        try:
            self.db.update_user_profile(key, value)
            self.memory[key] = value # Update local copy after successful DB update
        except Exception as e:
            logging.error(f"Error updating memory: {e}")