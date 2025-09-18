import re
from typing import Dict, Tuple
from nltk.tag import pos_tag # Requires NLTK installation: pip install nltk
from nltk.chunk import ne_chunk # Requires NLTK installation: pip install nltk
import nltk # Requires NLTK installation: pip install nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def extract_entities(text: str) -> list:
    """Extract named entities from text using NLTK."""
    tokens = nltk.word_tokenize(text)
    tagged = pos_tag(tokens)
    entities = []
    try:
        chunked = ne_chunk(tagged)
        for subtree in chunked.subtrees():
            if subtree.label() in ['PERSON', 'GPE', 'ORGANIZATION', 'LOCATION']:
                entities.append(' '.join([word for word, tag in subtree.leaves()]))
    except Exception as e:
        print(f"Error in entity extraction: {e}")
    return entities


def calculate_confidence(match: re.Match) -> float:
    """Calculate confidence based on match quality."""
    if match:
        span = match.end() - match.start()
        text_length = len(match.string)
        return min(1.0, span / text_length + 0.5)  # Adjust scaling as needed
    return 0.0


def parse_intent(user_input: str) -> Dict:
    """Parses user input and returns intent, entities, and confidence."""
    try:
        user_input = user_input.lower().strip()

        # More robust patterns (example - adjust as needed)
        patterns = {
            "open_app": r"(open|launch|start)\s+(\w+)",
            "close_app": r"(close|exit|stop)\s+(\w+)",
            "search_web": r"(search|look up|find)\s+(.*)",
            "generate_image": r"(generate|create|draw)\s+(image|picture|art)",
            "get_time": r"(what time|current time|tell me the time)",
            "get_date": r"(what date|today's date|current date)",
            "get_location": r"(where am i|my location|current location)",
            "control_wifi": r"(turn)\s+(on|off)\s+wifi",
            "control_bluetooth": r"(turn)\s+(on|off)\s+bluetooth",
            "system_action": r"(shutdown|restart|lock screen|power off)"
        }

        best_match = None
        best_confidence = 0.0

        for intent, pattern in patterns.items():
            match = re.search(pattern, user_input, re.IGNORECASE) #Added re.IGNORECASE
            if match:
                confidence = calculate_confidence(match)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = (intent, match)

        if best_match:
            intent, match = best_match
            entities = list(match.groups())
            entities.extend(extract_entities(user_input)) # Add extracted entities
            return {
                "intent": intent,
                "entities": entities,
                "confidence": best_confidence
            }
        else:
            return {
                "intent": "unknown",
                "entities": [],
                "confidence": 0.1
            }
    except Exception as e:
        print(f"Error parsing intent: {e}")
        return {"intent": "error", "entities": [], "confidence": 0.0}