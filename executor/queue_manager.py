# executor/queue_manager.py

import queue
import threading
import time

class TaskQueueManager:
    def __init__(self):
        self.task_queue = queue.PriorityQueue()
        self.running = False

    def add_task(self, priority: int, task: dict):
        """
        Adds a task to the queue with a given priority.
        Lower number = higher priority.
        """
        self.task_queue.put((priority, task))
        print(f"📝 Task added: {task['action']} (priority {priority})")

    def start_worker(self, executor):
        """
        Starts a background thread to process tasks.
        """
        if self.running:
            return

        self.running = True
        threading.Thread(target=self._worker_loop, args=(executor,), daemon=True).start()
        print("🚀 Task queue worker started.")

    def _worker_loop(self, executor):
        while self.running:
            if not self.task_queue.empty():
                priority, task = self.task_queue.get()
                try:
                    plugin_name = task.get("plugin")
                    action = task.get("action")
                    params = task.get("params", {})

                    plugin = executor.load_plugin(plugin_name)
                    method = getattr(plugin, action)
                    result = method(**params)

                    print(f"✅ Task completed: {action} → {result}")
                except Exception as e:
                    print(f"❌ Task failed: {action} → {e}")
            else:
                time.sleep(0.5)

    def stop_worker(self):
        self.running = False
        print("🛑 Task queue worker stopped.")
