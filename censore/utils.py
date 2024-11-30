from functools import lru_cache
from typing import Dict, FrozenSet

substitution_table: Dict[int, str] = str.maketrans(
    {
        "0": "o",
        "1": "i",
        "@": "a",
        "$": "s",
        "3": "e",
        "5": "s",
        "7": "t",
        "8": "b",
    }
)

strip_chars = ".,!?:;/()[]{}-"


@lru_cache(maxsize=None)
def load_patterns_from_file(filepath: str) -> FrozenSet[str]:
    """
    Loads patterns from a file and caches the result.

    Args:
        filepath: The path to the pattern file.

    Returns:
        A set of patterns loaded from the file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        patterns = frozenset(file.read().split())
    return patterns


@lru_cache(maxsize=None)
def normalize_word(word: str) -> str:
    """
    Normalize a word by translating it using the substitution table and converting it to lowercase.

    Args:
        word: The word to be normalized.

    Returns:
        The normalized word.
    """
    return word.translate(substitution_table).lower()


@lru_cache(maxsize=None)
def strip(word: str) -> str:
    """
    Strips specified punctuation characters from the beginning and end of the given word.

    Args:
        word: The word to be stripped of punctuation.

    Returns:
        The word with specified punctuation characters removed from its beginning and end.
    """
    return word.strip(strip_chars)
