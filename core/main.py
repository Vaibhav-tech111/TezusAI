# core/main.py
import os
import logging
from dotenv import load_dotenv
from brain.brain import TezusBrain
from executor.executor import TaskExecutor
from connectors.ai_models import AIModelFusion
from plugins import stt_tts

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Initialize core modules with dependency injection
def initialize_modules():
    brain = TezusBrain()
    executor = TaskExecutor(brain)
    fusion = AIModelFusion()
    return brain, executor, fusion

def startup_message():
    print("\nTezus is now active.")
    print("Say something or type a command...\n")

def main_loop():
    brain, executor, fusion = initialize_modules()
    startup_message()
    while True:
        try:
            # Listen via voice or text, handle potential errors
            user_input = stt_tts.listen()
            if not user_input:
                continue

            # Input sanitization (example - adapt as needed)
            user_input = user_input.strip()
            if not user_input:
                continue

            # Parse & plan
            task_plan = brain.plan(user_input)

            # Execute
            result = executor.run(task_plan)

            # Respond, handle potential errors
            stt_tts.speak(result)

        except KeyboardInterrupt:
            logging.info("Tezus shutting down.")
            break
        except ValueError as e:
            logging.error(f"Input validation error: {e}")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main_loop()