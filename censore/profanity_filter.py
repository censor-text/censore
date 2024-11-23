import os
from typing import List, Optional, Dict, FrozenSet, Set, Union
from functools import lru_cache


class ProfanityFilter:
    """
    A class used to filter profanity from text with support for multiple languages and custom patterns.

    Attributes:
        _substitution_table (Dict[int, str]): Translation table for character substitutions to normalize words.
        strip_chars (str): Characters to strip from words during normalization.
        _data_folder (str): Path to the data folder containing pattern files.
        languages (FrozenSet[str]): Set of languages for which profanity patterns are loaded.
        profanity_patterns (Dict[str, Dict[str, FrozenSet[str]]]): Dictionary storing profanity and exclusion patterns for each language.
    """

    # Translation table for character substitutions to normalize words
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
        languages: Union[FrozenSet[str], Set[str], List[str]] = frozenset(["all"]),
        custom_patterns: Union[FrozenSet[str], Set[str], List[str]] = [],
        custom_exclude_patterns: List[str] = [],
    ) -> None:
        """
        Initializes the profanity filter with specified languages and custom patterns.

        Args:
            languages (Union[FrozenSet[str], Set[str], List[str]], optional): A list of languages to load profanity patterns for. Defaults to frozenset(["all"]).
            custom_patterns (Union[FrozenSet[str], Set[str], List[str]], optional): A list of custom profanity patterns to add. Defaults to an empty list.
            custom_exclude_patterns (List[str], optional): A list of custom patterns to exclude from profanity filtering. Defaults to an empty list.
        """
        self.languages: FrozenSet[str] = frozenset()
        self.profanity_patterns: Dict[str, Dict[str, FrozenSet[str]]] = dict()

        # Load language patterns
        self._load_languages(languages)

        # Add custom patterns if provided
        if custom_patterns or custom_exclude_patterns:
            self.add_custom_profanity_patterns(custom_patterns, custom_exclude_patterns)

    def _load_languages(
        self,
        languages: Union[FrozenSet[str], Set[str], List[str]],
        is_additional_language: bool = False,
    ) -> None:
        """
        Loads language patterns for filtering.

        If the list of languages contains "all", it loads patterns for all available languages,
        using caching to improve performance.

        Args:
            languages (Union[FrozenSet[str], Set[str], List[str]]): List of language codes to load. If it contains "all",
                                   all available languages will be loaded.
            is_additional_language (bool, optional): Flag indicating whether the languages are additional.
                                                     Defaults to False.

        Raises:
            ValueError: If patterns for the specified language are not found.
        """
        # Determine which languages to load
        if "all" in languages:
            languages_for_loading = set(
                os.path.splitext(filename)[0]
                for filename in os.listdir(os.path.join(self._data_folder, "patterns"))
                if filename.endswith(".txt")
            )
        else:
            languages_for_loading = set(languages)

        # Load patterns for each language
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
            language (str): The language for which to load the patterns.
            is_additional_language (bool, optional): Flag indicating whether the language is
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
                "patterns": profanity_patterns,
                "exclude_patterns": exclude_patterns,
            }

            if not is_additional_language:
                self.languages = self.languages.union({language})

    @staticmethod
    @lru_cache(maxsize=None)
    def _load_patterns_from_file(filepath: str) -> FrozenSet[str]:
        """
        Loads patterns from a file and caches the result.

        Args:
            filepath (str): The path to the pattern file.

        Returns:
            FrozenSet[str]: A set of patterns loaded from the file.
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
            word (str): The word to be normalized.

        Returns:
            str: The normalized word.
        """
        # Translate characters using the substitution table and convert to lowercase
        return word.translate(ProfanityFilter._substitution_table).lower()

    @staticmethod
    @lru_cache(maxsize=None)
    def _strip(word: str) -> str:
        """
        Strips specified punctuation characters from the beginning and end of the given word.

        Args:
            word (str): The word to be stripped of punctuation.

        Returns:
            str: The word with specified punctuation characters removed from its beginning and end.
        """
        # Use the strip method with predefined characters to remove punctuation
        return word.strip(ProfanityFilter.strip_chars)

    def add_custom_profanity_patterns(
        self,
        custom_patterns: Union[FrozenSet[str], Set[str], List[str]],
        exclude_patterns: Union[FrozenSet[str], Set[str], List[str]],
        language: str = "custom",
    ) -> None:
        """
        Adds custom profanity patterns to the filter.

        Args:
            custom_patterns (Union[FrozenSet[str], Set[str], List[str]]): A list of custom profanity patterns to add.
            exclude_patterns (Union[FrozenSet[str], Set[str], List[str]]): A list of patterns to exclude from the profanity filter.
            language (str, optional): The language identifier for the custom patterns. Defaults to "custom".
        """
        self.add_custom_language(language, custom_patterns, exclude_patterns)

    def add_custom_language(
        self,
        language: str,
        custom_patterns: Union[FrozenSet[str], Set[str], List[str]],
        exclude_patterns: Union[FrozenSet[str], Set[str], List[str]],
    ) -> None:
        """
        Adds a custom language with specified profanity patterns and exclusion patterns.

        Args:
            language (str): The name of the language to add.
            custom_patterns (Union[FrozenSet[str], Set[str], List[str]]): A list of custom profanity patterns for the language.
            exclude_patterns (Union[FrozenSet[str], Set[str], List[str]]): A list of patterns to exclude from the profanity filter for the language.
        """
        # Use set operations for faster lookups and updates
        if language in self.profanity_patterns:
            # Update existing patterns and exclude patterns
            self.profanity_patterns[language]["patterns"] = self.profanity_patterns[
                language
            ]["patterns"].union(custom_patterns)
            self.profanity_patterns[language]["exclude_patterns"] = (
                self.profanity_patterns[language]["exclude_patterns"].union(
                    exclude_patterns
                )
            )
        else:
            # Initialize new language patterns and exclude patterns
            self.profanity_patterns[language] = {
                "patterns": frozenset(custom_patterns),
                "exclude_patterns": frozenset(exclude_patterns),
            }

        # Add the language to the set of languages if not already present
        self.languages = self.languages.union({language})

    def _load_all_pattern_sets(
        self,
        languages: FrozenSet[str],
        custom_patterns: Union[FrozenSet[str], Set[str], List[str]] = frozenset(),
        custom_exclude_patterns: Union[
            FrozenSet[str], Set[str], List[str]
        ] = frozenset(),
    ) -> Dict[str, FrozenSet[str]]:
        """
        Load and combine profanity patterns and exclude patterns for the specified languages.

        Args:
            languages (FrozenSet[str]): A list of language codes to load patterns for.
            custom_patterns (Union[FrozenSet[str], Set[str], List[str]], optional): A list of custom profanity patterns to include. Defaults to an empty list.
            custom_exclude_patterns (Union[FrozenSet[str], Set[str], List[str]], optional): A list of custom patterns to exclude. Defaults to an empty list.

        Returns:
            Dict[str, FrozenSet[str]]: A dictionary with two keys:
                - "patterns": A set of combined profanity patterns.
                - "exclude_patterns": A set of combined exclude patterns.
        """
        profanity_patterns: Set[str] = set()
        exclude_patterns: Set[str] = set()

        # Combine patterns from all specified languages
        for language in languages:
            patterns = self.profanity_patterns.get(language, {})
            profanity_patterns.update(patterns.get("patterns", []))
            exclude_patterns.update(patterns.get("exclude_patterns", []))

        # Add custom patterns
        profanity_patterns.update(custom_patterns)
        exclude_patterns.update(custom_exclude_patterns)

        return {
            "patterns": frozenset(profanity_patterns),
            "exclude_patterns": frozenset(exclude_patterns),
        }

    def _get_active_languages(
        self,
        languages: Optional[Union[FrozenSet[str], Set[str], List[str]]] = None,
        additional_languages: Optional[
            Union[FrozenSet[str], Set[str], List[str]]
        ] = None,
    ) -> FrozenSet[str]:
        """
        Get the list of active languages based on the provided languages and additional languages.

        Args:
            languages (Optional[Union[FrozenSet[str], Set[str], List[str]]]): A list of languages to be activated. If "all" is included, all available languages will be activated.
            additional_languages (Optional[Union[FrozenSet[str], Set[str], List[str]]]): A list of additional languages to be added to the active languages.

        Returns:
            FrozenSet[str]: A list of active languages.
        """
        # Start with the currently loaded languages
        active_languages = self.languages

        # Load specified languages if provided
        if languages:
            self._load_languages(languages)
            if "all" in languages:
                active_languages = self.languages
            else:
                active_languages = active_languages.union(
                    lang for lang in languages if lang not in active_languages
                )

        # Load additional languages if provided
        if additional_languages:
            self._load_languages(additional_languages, is_additional_language=True)
            active_languages = active_languages.union(
                lang for lang in additional_languages if lang not in active_languages
            )

        return frozenset(active_languages)

    def contains_profanity(
        self,
        text: str,
        languages: Optional[Union[FrozenSet[str], Set[str], List[str]]] = None,
        additional_languages: Optional[
            Union[FrozenSet[str], Set[str], List[str]]
        ] = None,
        custom_patterns: Union[FrozenSet[str], Set[str], List[str]] = frozenset(),
        custom_exclude_patterns: Union[
            FrozenSet[str], Set[str], List[str]
        ] = frozenset(),
    ) -> bool:
        """
        Checks if the given text contains any profanity.

        Args:
            text (str): The text to be checked for profanity.
            languages (Optional[Union[FrozenSet[str], Set[str], List[str]]], optional): List of languages to consider for profanity. Defaults to None.
            additional_languages (Optional[Union[FrozenSet[str], Set[str], List[str]]], optional): Additional languages to consider for profanity. Defaults to None.
            custom_patterns (Union[FrozenSet[str], Set[str], List[str]], optional): Custom patterns to be considered as profanity. Defaults to an empty list.
            custom_exclude_patterns (Union[FrozenSet[str], Set[str], List[str]], optional): Custom patterns to be excluded from profanity. Defaults to an empty list.

        Returns:
            bool: True if the text contains profanity, False otherwise.
        """
        # Get the active languages to be used for profanity detection
        active_languages = self._get_active_languages(languages, additional_languages)

        # Load all patterns for the active languages and custom patterns
        all_patterns = self._load_all_pattern_sets(
            active_languages, custom_patterns, custom_exclude_patterns
        )

        profanity_patterns = all_patterns["patterns"]
        exclude_patterns = all_patterns["exclude_patterns"]

        # Split the text into words
        words = text.split()

        # Check each word for profanity
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
        profanity_patterns: FrozenSet[str],
        exclude_patterns: FrozenSet[str],
    ) -> bool:
        """
        Check if a given word is considered profane based on provided patterns.

        Args:
            word (str): The word to check for profanity.
            profanity_patterns (FrozenSet[str]): A set of patterns that define profane words.
            exclude_patterns (FrozenSet[str]): A set of patterns that define words to exclude from being considered profane.

        Returns:
            bool: True if the word is considered profane, False otherwise.
        """
        normalized_word = self._normalize_word(self._strip(word))

        # Check if the word is in the exclude patterns
        if any(map(normalized_word.__contains__, exclude_patterns)):
            return False

        # Check if the word is in the profanity patterns
        return any(map(normalized_word.__contains__, profanity_patterns))

    @lru_cache(maxsize=None)
    def censor_word(
        self, word: str, partial_censor: bool = False, censoring_char: str = "#"
    ) -> str:
        """
        Censors a given word by replacing its characters with a specified censoring character.

        Args:
            word (str): The word to be censored.
            partial_censor (bool, optional): If True, only partially censors the word, keeping the first and last characters intact. Defaults to False.
            censoring_char (str, optional): The character used for censoring. Defaults to "#".

        Returns:
            str: The censored word.
        """
        word_length = len(word)

        if partial_censor and word_length > 2:
            return f"{word[0]}{censoring_char * (word_length - 2)}{word[-1]}"
        return censoring_char * word_length

    def censor(
        self,
        text: str,
        languages: Optional[Union[FrozenSet[str], Set[str], List[str]]] = None,
        additional_languages: Optional[
            Union[FrozenSet[str], Set[str], List[str]]
        ] = None,
        custom_patterns: Union[FrozenSet[str], Set[str], List[str]] = frozenset(),
        custom_exclude_patterns: Union[
            FrozenSet[str], Set[str], List[str]
        ] = frozenset(),
        partial_censor: bool = False,
        censor_symbol: str = "#",
    ) -> str:
        """
        Censors profane words in the given text based on specified languages and custom patterns.

        Args:
            text (str): The input text to be censored.
            languages (Optional[Union[FrozenSet[str], Set[str], List[str]]]): List of languages to use for profanity detection.
            additional_languages (Optional[Union[FrozenSet[str], Set[str], List[str]]]): Additional languages to include for profanity detection.
            custom_patterns (Union[FrozenSet[str], Set[str], List[str]]): List of custom patterns to be considered as profane.
            custom_exclude_patterns (Union[FrozenSet[str], Set[str], List[str]]): List of custom patterns to be excluded from being considered as profane.
            partial_censor (bool): If True, partially censors the profane words. Defaults to False.
            censor_symbol (str): The symbol used to replace profane words. Defaults to "#".

        Returns:
            str: The censored version of the input text.
        """
        active_languages = self._get_active_languages(
            frozenset(languages) if languages else None,
            frozenset(additional_languages) if additional_languages else None,
        )

        all_patterns = self._load_all_pattern_sets(
            active_languages, custom_patterns, custom_exclude_patterns
        )

        profanity_patterns = all_patterns["patterns"]
        exclude_patterns = all_patterns["exclude_patterns"]

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
