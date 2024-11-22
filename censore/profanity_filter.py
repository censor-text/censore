import string
import os
from typing import List, Optional, Dict, Set


class ProfanityFilter:
    _substitution_table = str.maketrans(
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

    _data_folder = os.path.join(os.path.dirname(__file__), "data")

    def __init__(
        self,
        languages: List[str] = ["all"],
        custom_patterns: List[str] = [],
        custom_exclude_patterns: List[str] = [],
    ) -> None:
        """
        Initializes the profanity filter with specified languages and custom patterns.

        Args:
            languages (List[str], optional): A list of languages to load profanity patterns for. Defaults to ["all"].
            custom_patterns (List[str], optional): A list of custom profanity patterns to add. Defaults to an empty list.
            custom_exclude_patterns (List[str], optional): A list of custom patterns to exclude from profanity filtering. Defaults to an empty list.
        """

        self.languages: List[str] = []
        self.profanity_patterns = {}

        self._load_languages(languages)

        if custom_patterns or custom_exclude_patterns:
            self.add_custom_profanity_patterns(custom_patterns, custom_exclude_patterns)

    def _load_languages(
        self, languages: List[str], is_additional_language: bool = False
    ) -> None:
        """
        Load language patterns for the profanity filter.

        This method loads language patterns from the specified list of languages.
        If "all" is included in the list, it loads patterns for all available languages.

        Args:
            languages (List[str]): A list of language codes to load. If "all" is included,
                                   all available languages will be loaded.
            is_additional_language (bool, optional): A flag indicating whether the languages
                                                     being loaded are additional languages.
                                                     Defaults to False.

        Returns:
            None
        """

        languages_for_loading = []

        if "all" in languages:
            for filename in os.listdir(os.path.join(self._data_folder, "patterns")):
                if filename.endswith(".txt"):
                    languages_for_loading.append(os.path.splitext(filename)[0])
        else:
            languages_for_loading = languages

        for language in languages_for_loading:
            self._load_language(language, is_additional_language)

    def _load_language(
        self, language: str, is_additional_language: bool = False
    ) -> None:
        """
        Loads profanity and exclusion patterns for a given language.

        This method reads profanity and exclusion patterns from text files located in the
        data folder and stores them in the `profanity_patterns` dictionary. If the language
        is not marked as an additional language, it is also added to the `languages` list.

        Args:
            language (str): The language for which to load the patterns.
            is_additional_language (bool, optional): Flag indicating whether the language is
                an additional language. Defaults to False.

        Returns:
            None
        """
        if language not in self.languages:
            path_to_profanity_patterns = os.path.join(
                self._data_folder, "patterns", f"{language}.txt"
            )
            path_to_exclude_patterns = os.path.join(
                self._data_folder, "exclude_patterns", f"{language}.txt"
            )

            with open(
                path_to_profanity_patterns, "r", encoding="utf-8"
            ) as file_with_profanity_patterns, open(
                path_to_exclude_patterns, "r", encoding="utf-8"
            ) as file_with_exclude_patterns:
                profanity_patterns = file_with_profanity_patterns.read().split()
                exclude_patterns = file_with_exclude_patterns.read().split()

            self.profanity_patterns[language] = {
                "patterns": profanity_patterns,
                "exclude_patterns": exclude_patterns,
            }

            if not is_additional_language:
                self.languages.append(language)

    @staticmethod
    def _normalize_word(word: str) -> str:
        """
        Normalize a word by translating it using the substitution table and converting it to lowercase.

        Args:
            word (str): The word to be normalized.

        Returns:
            str: The normalized word.
        """
        return word.translate(ProfanityFilter._substitution_table).lower()

    @staticmethod
    def _strip(word: str) -> str:
        """
        Strips specified punctuation characters from the beginning and end of the given word.

        Args:
            word (str): The word to be stripped of punctuation.

        Returns:
            str: The word with specified punctuation characters removed from its beginning and end.
        """
        return word.strip(".,!?:;/()[]{}-")

    def add_custom_profanity_patterns(
        self,
        custom_patterns: List[str],
        exclude_patterns: List[str],
        language: str = "custom",
    ) -> None:
        """
        Adds custom profanity patterns to the filter.

        Args:
            custom_patterns (List[str]): A list of custom profanity patterns to add.
            exclude_patterns (List[str]): A list of patterns to exclude from the profanity filter.
            language (str, optional): The language identifier for the custom patterns. Defaults to "custom".

        Returns:
            None
        """

        self.add_custom_language(language, custom_patterns, exclude_patterns)

    def add_custom_language(
        self, language: str, custom_patterns: List[str], exclude_patterns: List[str]
    ) -> None:
        """
        Adds a custom language with specified profanity patterns and exclusion patterns.

        Args:
            language (str): The name of the language to add.
            custom_patterns (List[str]): A list of custom profanity patterns for the language.
            exclude_patterns (List[str]): A list of patterns to exclude from the profanity filter for the language.

        Returns:
            None
        """

        self.profanity_patterns[language] = {
            "patterns": custom_patterns,
            "exclude_patterns": exclude_patterns,
        }

        if language not in self.languages:
            self.languages.append(language)

    def _load_all_pattern_sets(
        self,
        languages: List[str],
        custom_patterns: List[str] = [],
        custom_exclude_patterns: List[str] = [],
    ) -> Dict[str, Set[str]]:
        """
        Load and combine profanity patterns and exclude patterns for the specified languages.

        Args:
            languages (List[str]): A list of language codes to load patterns for.
            custom_patterns (List[str], optional): A list of custom profanity patterns to include. Defaults to an empty list.
            custom_exclude_patterns (List[str], optional): A list of custom patterns to exclude. Defaults to an empty list.

        Returns:
            Dict[str, Set[str]]: A dictionary with two keys:
                - "patterns": A set of combined profanity patterns.
                - "exclude_patterns": A set of combined exclude patterns.
        """

        profanity_patterns = set()
        exclude_patterns = set()

        for language in languages:
            patterns = self.profanity_patterns.get(language, {})
            profanity_patterns.update(patterns.get("patterns", []))
            exclude_patterns.update(patterns.get("exclude_patterns", []))

        profanity_patterns.update(custom_patterns)
        exclude_patterns.update(custom_exclude_patterns)

        return {"patterns": profanity_patterns, "exclude_patterns": exclude_patterns}

    def _get_active_languages(
        self,
        languages: Optional[List[str]] = None,
        additional_languages: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Get the list of active languages based on the provided languages and additional languages.

        Args:
            languages (Optional[List[str]]): A list of languages to be activated. If "all" is included, all available languages will be activated.
            additional_languages (Optional[List[str]]): A list of additional languages to be added to the active languages.

        Returns:
            List[str]: A list of active languages.
        """

        active_languages = list(self.languages)

        if languages:
            self._load_languages(languages)
            if "all" in languages:
                active_languages = self.languages
            else:
                active_languages = languages

        if additional_languages:
            self._load_languages(additional_languages, is_additional_language=True)
            active_languages += additional_languages

        return active_languages

    def contains_profanity(
        self,
        text: str,
        languages: Optional[List[str]] = None,
        additional_languages: Optional[List[str]] = None,
        custom_patterns: List[str] = [],
        custom_exclude_patterns: List[str] = [],
    ) -> bool:
        """
        Checks if the given text contains any profanity.

        Args:
            text (str): The text to be checked for profanity.
            languages (Optional[List[str]], optional): List of languages to consider for profanity. Defaults to None.
            additional_languages (Optional[List[str]], optional): Additional languages to consider for profanity. Defaults to None.
            custom_patterns (List[str], optional): Custom patterns to be considered as profanity. Defaults to an empty list.
            custom_exclude_patterns (List[str], optional): Custom patterns to be excluded from profanity. Defaults to an empty list.

        Returns:
            bool: True if the text contains profanity, False otherwise.
        """

        active_languages = self._get_active_languages(languages, additional_languages)

        all_patterns = self._load_all_pattern_sets(
            active_languages, custom_patterns, custom_exclude_patterns
        )

        profanity_patterns = all_patterns["patterns"]
        exclude_patterns = all_patterns["exclude_patterns"]

        lines = text.split()

        for word in lines:
            if self._is_profane_word(
                word,
                profanity_patterns=profanity_patterns,
                exclude_patterns=exclude_patterns,
            ):
                return True
        return False

    def _is_profane_word(
        self,
        word: str,
        profanity_patterns: Set[str],
        exclude_patterns: Set[str],
    ) -> bool:
        """
        Check if a given word is considered profane based on provided patterns.

        Args:
            word (str): The word to check for profanity.
            profanity_patterns (Set[str]): A set of patterns that define profane words.
            exclude_patterns (Set[str]): A set of patterns that define words to exclude from being considered profane.

        Returns:
            bool: True if the word is considered profane, False otherwise.
        """

        normalized_word = self._normalize_word(self._strip(word))

        if not any(pattern in normalized_word for pattern in exclude_patterns) and any(
            pattern in normalized_word for pattern in profanity_patterns
        ):
            return True
        return False

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

        if partial_censor:
            if len(word) > 2:
                return word[0] + censoring_char * (len(word) - 2) + word[-1]
            else:
                return censoring_char * len(word)
        else:
            return censoring_char * len(word)

    def censor(
        self,
        text: str,
        languages: Optional[List[str]] = None,
        additional_languages: Optional[List[str]] = None,
        custom_patterns: List[str] = [],
        custom_exclude_patterns: List[str] = [],
        partial_censor: bool = False,
        censor_symbol: str = "#",
    ) -> str:
        """
        Censors profane words in the given text based on specified languages and custom patterns.

        Args:
            text (str): The input text to be censored.
            languages (Optional[List[str]]): List of languages to use for profanity detection.
            additional_languages (Optional[List[str]]): Additional languages to include for profanity detection.
            custom_patterns (List[str]): List of custom patterns to be considered as profane.
            custom_exclude_patterns (List[str]): List of custom patterns to be excluded from being considered as profane.
            partial_censor (bool): If True, partially censors the profane words. Defaults to False.
            censor_symbol (str): The symbol used to replace profane words. Defaults to "#".

        Returns:
            str: The censored version of the input text.
        """

        active_languages = self._get_active_languages(languages, additional_languages)

        all_patterns = self._load_all_pattern_sets(
            active_languages, custom_patterns, custom_exclude_patterns
        )

        profanity_patterns = all_patterns["patterns"]
        exclude_patterns = all_patterns["exclude_patterns"]

        words = text.split()
        censored_text = text

        for word in words:
            stripped_word = self._strip(word)

            normalized_word = self._normalize_word(word)
            if self._is_profane_word(
                normalized_word,
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
