# brain/fusion.py

from typing import List, Dict
import difflib

def calculate_similarity_matrix(responses: List[str]) -> List[tuple]:
    """Calculates a similarity matrix for a list of strings."""
    similarity_matrix = []
    try:
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                score = difflib.SequenceMatcher(None, responses[i], responses[j]).ratio()
                similarity_matrix.append((i, j, score))
    except TypeError:
        return [] # Handle non-string inputs gracefully

    return similarity_matrix


def fuse_results(responses: List[str]) -> str:
    """Combines multiple AI model responses into a single, refined output."""

    if not responses:
        return "I'm sorry, I couldn't generate a response."

    if len(responses) == 1:
        return responses[0]

    similarity_matrix = calculate_similarity_matrix(responses)

    if not similarity_matrix:
        return responses[0] #Fallback if similarity calculation fails

    scores = [0] * len(responses)
    for i, j, score in similarity_matrix:
        scores[i] += score
        scores[j] += score

    best_index = scores.index(max(scores))
    best_response = responses[best_index]

    summary = summarize_variants(responses, best_index)

    return f"{best_response}\n\n* Summary from other models:\n{summary}" if summary else best_response


def summarize_variants(responses: List[str], exclude_index: int) -> str:
    """Summarizes alternative responses for transparency."""
    variants = [r for i, r in enumerate(responses) if i != exclude_index]
    if not variants:
        return ""

    return "\n".join([f"- {v}" for v in variants])