# core/main.py

import os
from dotenv import load_dotenv
from brain.brain import TezusBrain
from executor.executor import TaskExecutor
from connectors.ai_models import AIModelFusion
from plugins import stt_tts

# Load environment variables
load_dotenv()

# Initialize core modules
brain = TezusBrain()
executor = TaskExecutor(brain)
fusion = AIModelFusion()

def startup_message():
    print("\n✨ Tezus is now active.")
    print("🎙️ Say something or type a command...\n")

def main_loop():
    startup_message()
    while True:
        try:
            # Listen via voice or text
            user_input = stt_tts.listen()  # You can replace with input() for CLI
            if not user_input:
                continue

            # Parse & plan
            task_plan = brain.plan(user_input)

            # Execute
            result = executor.run(task_plan)

            # Respond
            stt_tts.speak(result)

        except KeyboardInterrupt:
            print("\n🛑 Tezus shutting down.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main_loop()
