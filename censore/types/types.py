from dataclasses import dataclass
from typing import Optional


@dataclass
class Word:
    original: str
    censored: str
    is_profane: Optional[bool]

    def __str__(self) -> str:
        return self.censored


@dataclass
class Text(Word):
    words_censored: int
