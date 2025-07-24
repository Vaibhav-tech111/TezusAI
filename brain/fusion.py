# brain/fusion.py

from typing import List, Dict
import difflib

def fuse_results(responses: List[str]) -> str:
    """
    Combines multiple AI model responses into a single, refined output.
    """

    if not responses:
        return "I'm sorry, I couldn't generate a response."

    # If only one response, return it
    if len(responses) == 1:
        return responses[0]

    # Step 1: Score similarity between responses
    similarity_matrix = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            score = difflib.SequenceMatcher(None, responses[i], responses[j]).ratio()
            similarity_matrix.append((i, j, score))

    # Step 2: Choose most consistent response
    scores = [0] * len(responses)
    for i, j, score in similarity_matrix:
        scores[i] += score
        scores[j] += score

    best_index = scores.index(max(scores))
    best_response = responses[best_index]

    # Step 3: Optionally summarize others
    summary = summarize_variants(responses, best_index)

    return f"{best_response}\n\n🧠 Summary from other models:\n{summary}" if summary else best_response

def summarize_variants(responses: List[str], exclude_index: int) -> str:
    """
    Summarizes alternative responses for transparency.
    """
    variants = [r for i, r in enumerate(responses) if i != exclude_index]
    if not variants:
        return ""

    # Simple merge or bullet points
    return "\n".join([f"- {v}" for v in variants])
