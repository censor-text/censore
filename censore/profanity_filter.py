import os
from typing import List, Optional, Dict, FrozenSet, Set, Union, Iterable
from functools import lru_cache


class ProfanityFilter:
    """
    A class used to filter profanity from text with support for multiple languages and custom patterns.

    Attributes:
        _substitution_table: Translation table for character substitutions to normalize words.
        strip_chars: Characters to strip from words during normalization.
        _data_folder: Path to the data folder containing pattern files.
        languages: Set of languages for which profanity patterns are loaded.
        profanity_patterns: Dictionary storing profanity and exclusion patterns for each language.
    """

    _substitution_table: Dict[int, str] = str.maketrans(
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

    strip_chars: str = ".,!?:;/()[]{}-"

    # Path to the data folder containing pattern files
    _data_folder: str = os.path.join(os.path.dirname(__file__), "data")

    def __init__(
        self,
        languages: Iterable[str] = frozenset(["all"]),
        custom_patterns: Iterable[str] = frozenset(),
        custom_exclude_patterns: Iterable[str] = frozenset(),
    ) -> None:
        """
        Initializes the profanity filter with specified languages and custom patterns.

        Args:
            languages: A list of languages to load profanity patterns for. Defaults to frozenset(["all"]).
            custom_patterns: A list of custom profanity patterns to add. Defaults to an empty list.
            custom_exclude_patterns: A list of custom patterns to exclude from profanity filtering. Defaults to an empty list.
        """
        self.languages: Set[str] = set()
        self.profanity_patterns: Dict[str, Dict[str, Set[str]]] = dict()

        self._load_languages(languages)

        if custom_patterns or custom_exclude_patterns:
            self.add_custom_profanity_patterns(custom_patterns, custom_exclude_patterns)

    def _load_languages(
        self,
        languages: Iterable[str] = frozenset(),
        is_additional_language: bool = False,
    ) -> None:
        """
        Loads language patterns for filtering.

        If the list of languages contains "all", it loads patterns for all available languages,
        using caching to improve performance.

        Args:
            languages: List of language codes to load. If it contains "all",
                       all available languages will be loaded.
            is_additional_language: Flag indicating whether the languages are additional.
                                    Defaults to False.

        Raises:
            ValueError: If patterns for the specified language are not found.
        """
        if "all" in languages:
            languages_for_loading = set(
                os.path.splitext(filename)[0]
                for filename in os.listdir(os.path.join(self._data_folder, "patterns"))
                if filename.endswith(".txt")
            )
        else:
            languages_for_loading = frozenset(languages)

        for language in languages_for_loading:
            try:
                self._load_language(language, is_additional_language)
            except FileNotFoundError:
                raise ValueError(f"Patterns for language '{language}' not found")

    def _load_language(
        self, language: str, is_additional_language: bool = False
    ) -> None:
        """
        Loads profanity and exclusion patterns for a given language.

        Args:
            language: The language for which to load the patterns.
            is_additional_language: Flag indicating whether the language is
                                    an additional language. Defaults to False.
        """
        if language not in self.languages:
            path_to_profanity_patterns = os.path.join(
                self._data_folder, "patterns", f"{language}.txt"
            )
            path_to_exclude_patterns = os.path.join(
                self._data_folder, "exclude_patterns", f"{language}.txt"
            )

            profanity_patterns = self._load_patterns_from_file(
                path_to_profanity_patterns
            )
            exclude_patterns = self._load_patterns_from_file(path_to_exclude_patterns)

            self.profanity_patterns[language] = {
                "patterns": set(profanity_patterns),
                "exclude_patterns": set(exclude_patterns),
            }

            if not is_additional_language:
                self.languages.update({language})

    @staticmethod
    @lru_cache(maxsize=None)
    def _load_patterns_from_file(filepath: str) -> FrozenSet[str]:
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

    @staticmethod
    @lru_cache(maxsize=None)
    def _normalize_word(word: str) -> str:
        """
        Normalize a word by translating it using the substitution table and converting it to lowercase.

        Args:
            word: The word to be normalized.

        Returns:
            The normalized word.
        """
        return word.translate(ProfanityFilter._substitution_table).lower()

    @staticmethod
    @lru_cache(maxsize=None)
    def _strip(word: str) -> str:
        """
        Strips specified punctuation characters from the beginning and end of the given word.

        Args:
            word: The word to be stripped of punctuation.

        Returns:
            The word with specified punctuation characters removed from its beginning and end.
        """
        return word.strip(ProfanityFilter.strip_chars)

    def add_custom_profanity_patterns(
        self,
        custom_patterns: Iterable[str],
        exclude_patterns: Iterable[str],
        language: str = "custom",
    ) -> None:
        """
        Adds custom profanity patterns to the filter.

        Args:
            custom_patterns: A list of custom profanity patterns to add.
            exclude_patterns: A list of patterns to exclude from the profanity filter.
            language: The language identifier for the custom patterns. Defaults to "custom".
        """
        self.add_custom_language(language, custom_patterns, exclude_patterns)

    def add_custom_language(
        self,
        language: str,
        custom_patterns: Iterable[str] = frozenset(),
        exclude_patterns: Iterable[str] = frozenset(),
    ) -> None:
        """
        Adds a custom language with specified profanity patterns and exclusion patterns.

        Args:
            language: The name of the language to add.
            custom_patterns: A list of custom profanity patterns for the language.
            exclude_patterns: A list of patterns to exclude from the profanity filter for the language.
        """
        if language in self.profanity_patterns:
            self.profanity_patterns[language]["patterns"].update(custom_patterns)
            self.profanity_patterns[language]["exclude_patterns"].union(
                exclude_patterns
            )

        else:
            self.profanity_patterns[language] = {
                "patterns": set(custom_patterns),
                "exclude_patterns": set(exclude_patterns),
            }

        self.languages = self.languages.union({language})

    def _load_all_pattern_sets(
        self,
        languages: Optional[Iterable[str]] = None,
        custom_patterns: Optional[Iterable[str]] = frozenset(),
        custom_exclude_patterns: Optional[Iterable[str]] = frozenset(),
    ) -> Dict[str, Set[str]]:
        """
        Load and combine profanity patterns and exclude patterns for the specified languages.

        Args:
            languages: A list of language codes to load patterns for.
            custom_patterns: A list of custom profanity patterns to include. Defaults to an empty list.
            custom_exclude_patterns: A list of custom patterns to exclude. Defaults to an empty list.

        Returns:
            A dictionary with two keys:
                - "patterns": A set of combined profanity patterns.
                - "exclude_patterns": A set of combined exclude patterns.

        Raises:
            ValueError: If no languages are specified for loading patterns.
        """
        profanity_patterns: Set[str] = set()
        exclude_patterns: Set[str] = set()

        if languages:
            for language in languages:
                patterns = self.profanity_patterns.get(language, {})
                profanity_patterns.update(patterns.get("patterns", []))
                exclude_patterns.update(patterns.get("exclude_patterns", []))

            if custom_patterns:
                profanity_patterns.update(frozenset(custom_patterns))

            if custom_exclude_patterns:
                exclude_patterns.update(frozenset(custom_exclude_patterns))

            return {
                "patterns": profanity_patterns,
                "exclude_patterns": exclude_patterns,
            }
        else:
            raise ValueError("No languages specified for loading patterns")

    def _get_active_languages(
        self,
        languages: Optional[Iterable[str]] = None,
        additional_languages: Optional[Iterable[str]] = None,
    ) -> Set[str]:
        """
        Get the list of active languages based on the provided languages and additional languages.

        Args:
            languages: A list of languages to be activated. If "all" is included, all available languages will be activated.
            additional_languages: A list of additional languages to be added to the active languages.

        Returns:
            A list of active languages.
        """
        active_languages = self.languages

        if languages:
            self._load_languages(languages)
            if not "all" in languages:
                active_languages.update(languages)

        if additional_languages:
            self._load_languages(additional_languages, is_additional_language=True)
            active_languages.union(additional_languages)

        return active_languages

    def contains_profanity(
        self,
        text: str,
        languages: Optional[Iterable[str]] = None,
        additional_languages: Optional[Iterable[str]] = None,
        custom_patterns: Optional[Iterable[str]] = None,
        custom_exclude_patterns: Optional[Iterable[str]] = None,
    ) -> bool:
        """
        Checks if the given text contains any profanity.

        Args:
            text: The text to be checked for profanity.
            languages: List of languages to consider for profanity. Defaults to None.
            additional_languages: Additional languages to consider for profanity. Defaults to None.
            custom_patterns: Custom patterns to be considered as profanity. Defaults to an empty list.
            custom_exclude_patterns: Custom patterns to be excluded from profanity. Defaults to an empty list.

        Returns:
            True if the text contains profanity, False otherwise.
        """
        active_languages = self._get_active_languages(languages, additional_languages)

        all_patterns = self._load_all_pattern_sets(
            active_languages, custom_patterns, custom_exclude_patterns
        )

        profanity_patterns = frozenset(all_patterns["patterns"])
        exclude_patterns = frozenset(all_patterns["exclude_patterns"])

        words = text.split()

        for word in words:
            if self._is_profane_word(
                word,
                profanity_patterns=profanity_patterns,
                exclude_patterns=exclude_patterns,
            ):
                return True

        return False

    @lru_cache(maxsize=None)
    def _is_profane_word(
        self,
        word: str,
        profanity_patterns: Iterable[str],
        exclude_patterns: Iterable[str],
    ) -> bool:
        """
        Check if a given word is considered profane based on provided patterns.

        Args:
            word: The word to check for profanity.
            profanity_patterns: A set of patterns that define profane words.
            exclude_patterns: A set of patterns that define words to exclude from being considered profane.

        Returns:
            True if the word is considered profane, False otherwise.
        """
        normalized_word = self._normalize_word(self._strip(word))

        for pattern in exclude_patterns:
            if pattern in normalized_word:
                return False

        for profanity_pattern in profanity_patterns:
            if profanity_pattern in normalized_word:
                return True

        # Temporary type fix
        return False

    @lru_cache(maxsize=None)
    def censor_word(
        self, word: str, partial_censor: bool = False, censoring_char: str = "#"
    ) -> str:
        """
        Censors a given word by replacing its characters with a specified censoring character.

        Args:
            word: The word to be censored.
            partial_censor: If True, only partially censors the word, keeping the first and last characters intact. Defaults to False.
            censoring_char: The character used for censoring. Defaults to "#".

        Returns:
            The censored word.
        """
        word_length = len(word)

        if partial_censor and word_length > 2:
            return f"{word[0]}{censoring_char * (word_length - 2)}{word[-1]}"
        return censoring_char * word_length

    def censor(
        self,
        text: str,
        languages: Optional[Iterable[str]] = None,
        additional_languages: Optional[Iterable[str]] = None,
        custom_patterns: Optional[Iterable[str]] = None,
        custom_exclude_patterns: Optional[Iterable[str]] = None,
        partial_censor: bool = False,
        censor_symbol: str = "#",
    ) -> str:
        """
        Censors profane words in the given text based on specified languages and custom patterns.

        Args:
            text: The input text to be censored.
            languages: List of languages to use for profanity detection.
            additional_languages: Additional languages to include for profanity detection.
            custom_patterns: List of custom patterns to be considered as profane.
            custom_exclude_patterns: List of custom patterns to be excluded from being considered as profane.
            partial_censor: If True, partially censors the profane words. Defaults to False.
            censor_symbol: The symbol used to replace profane words. Defaults to "#".

        Returns:
            The censored version of the input text.
        """
        active_languages = self._get_active_languages(
            languages,
            additional_languages,
        )

        all_patterns = self._load_all_pattern_sets(
            active_languages, custom_patterns, custom_exclude_patterns
        )

        profanity_patterns = frozenset(all_patterns["patterns"])
        exclude_patterns = frozenset(all_patterns["exclude_patterns"])

        words = text.split()
        censored_text = text

        for word in words:
            stripped_word = self._strip(word)

            if self._is_profane_word(
                word,
                profanity_patterns=profanity_patterns,
                exclude_patterns=exclude_patterns,
            ):
                censored_word = self.censor_word(
                    stripped_word,
                    partial_censor=partial_censor,
                    censoring_char=censor_symbol,
                )
                censored_text = censored_text.replace(stripped_word, censored_word)
        return censored_text
