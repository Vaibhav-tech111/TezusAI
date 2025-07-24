# executor/executor.py

import importlib
from brain.fusion import fuse_results

class TaskExecutor:
    def __init__(self, brain):
        self.brain = brain
        self.loaded_plugins = {}

    def run(self, task_plan: list) -> str:
        results = []

        for step in task_plan:
            plugin_name = step.get("plugin")
            action = step.get("action")
            params = step.get("params", {})

            try:
                plugin = self.load_plugin(plugin_name)
                method = getattr(plugin, action)
                result = method(**params)
                results.append(result)

            except Exception as e:
                results.append(f"⚠️ Error in {plugin_name}.{action}: {e}")

        # Fuse results if multiple
        return self.brain.fuse(results)

    def load_plugin(self, plugin_name: str):
        """
        Dynamically loads plugin module and caches it.
        """
        if plugin_name in self.loaded_plugins:
            return self.loaded_plugins[plugin_name]

        try:
            module = importlib.import_module(f"plugins.{plugin_name}")
            self.loaded_plugins[plugin_name] = module
            return module
        except ImportError as e:
            raise Exception(f"Plugin '{plugin_name}' not found: {e}")
