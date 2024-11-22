import string
import os


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
        languages: list[str] = ["all"],
        custom_patterns: list[str] = [],
        custom_exclude_patterns: list[str] = [],
    ):
        """
        Initializes the profanity filter with specified languages and custom patterns.

        Args:
            languages (list[str], optional): List of languages to load profanity patterns for. Defaults to ["all"].
            custom_patterns (list[str], optional): List of custom profanity patterns to add. Defaults to an empty list.
            custom_exclude_patterns (list[str], optional): List of custom patterns to exclude from the profanity filter. Defaults to an empty list.
        """

        # Initialize the profanity patterns dictionary
        self.languages: list[str] = []
        self.profanity_patterns = {}

        # Load the profanity patterns
        self._load_languages(languages)

        if custom_patterns:
            self.add_custom_patterns(custom_patterns, custom_exclude_patterns)

    def _load_languages(
        self, languages: list[str], is_additional: bool = False
    ) -> None:
        """
        Loads language patterns for profanity filtering.

        This method loads language patterns from the specified list of languages.
        If "all" is specified in the languages list, it loads all available language
        patterns from the patterns directory. Otherwise, it loads the specified languages.

        Args:
            languages (list[str]): A list of language codes to load. If "all" is included,
                                   all available languages will be loaded.
            is_additional (bool, optional): A flag indicating whether the languages being
                                            loaded are additional to the existing ones.
                                            Defaults to False.

        Returns:
            None
        """
        languages_for_loading = []

        # Load languages
        if "all" in languages:
            for filename in os.listdir(os.path.join(self._data_folder, "patterns")):
                if filename.endswith(".txt"):
                    languages_for_loading.append(os.path.splitext(filename)[0])
        else:
            languages_for_loading = languages

        for language in languages_for_loading:
            self._load_language(language, is_additional)

    def _load_language(self, language: str, is_additional: bool = False) -> None:
        """
        Loads profanity and exclusion patterns for a specified language.

        This method reads profanity and exclusion patterns from text files located in the
        data folder and stores them in the profanity_patterns dictionary. If the language
        is not marked as additional, it is also appended to the languages list.

        Args:
            language (str): The language for which to load the patterns.
            is_additional (bool, optional): Flag indicating whether the language is additional.
                                            Defaults to False.

        Raises:
            FileNotFoundError: If the pattern files for the specified language do not exist.
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

            if not is_additional:
                self.languages.append(language)

    @staticmethod
    def _normalize_word(word: str) -> str:
        """
        Normalizes a word by substituting characters according to the substitution table
        and removing punctuation.

        :param word: The word to normalize.
        :return: The normalized word.
        """
        return word.translate(ProfanityFilter._substitution_table).lower()

    @staticmethod
    def _strip(word: str) -> str:
        """
        Strips punctuation from the beginning and end of a word.

        :param word: The word to strip.
        :return: The stripped word.
        """
        return word.strip(".,!?:;/()[]{}-")

    def add_custom_patterns(
        self,
        custom_patterns: list[str],
        exclude_patterns: list[str],
        language: str = "custom",
    ) -> None:
        """
        Adds custom profanity patterns to the filter.

        Args:
            custom_patterns (list[str]): A list of custom patterns to be added.
            exclude_patterns (list[str]): A list of patterns to be excluded.
            language (str, optional): The language identifier for the custom patterns. Defaults to "custom".

        Returns:
            None
        """
        self.add_custom_lang(language, custom_patterns, exclude_patterns)

    def add_custom_lang(
        self, language: str, custom_patterns: list[str], exclude_patterns: list[str]
    ) -> None:
        """
        Adds a custom language with specific profanity patterns and exclusion patterns.

        Args:
            language (str): The name of the language to add.
            custom_patterns (list[str]): A list of custom profanity patterns for the language.
            exclude_patterns (list[str]): A list of patterns to exclude from the profanity filter for the language.

        Returns:
            None
        """

        if language not in self.profanity_patterns:
            self.profanity_patterns[language] = {}

        self.profanity_patterns[language] = {
            "patterns": custom_patterns,
            "exclude_patterns": exclude_patterns,
        }

        if language not in self.languages:
            self.languages.append(language)

    def contains_profanity(
        self,
        text: str,
        languages: list[str] = None,
        additional_languages: list[str] = None,
        custom_patterns: list[str] = [],
        custom_exclude_patterns: list[str] = [],
    ) -> bool:
        """
        Checks if the given text contains any profanity based on specified or default languages and patterns.

        Args:
            text (str): The text to be checked for profanity.
            languages (list[str], optional): A list of languages to check for profanity. If "all" is included, all available languages will be checked. Defaults to None.
            additional_languages (list[str], optional): Additional languages to check for profanity, without replacing the default languages. Defaults to None.
            custom_patterns (list[str], optional): Custom patterns to be considered as profanity. Defaults to an empty list.
            custom_exclude_patterns (list[str], optional): Custom patterns to be excluded from being considered as profanity. Defaults to an empty list.

        Returns:
            bool: True if the text contains profanity, False otherwise.
        """

        # Ensure all specified languages are loaded
        active_languages = list(self.languages)  # Clone the current languages

        if languages:
            self._load_languages(languages)

            if "all" in languages:
                active_languages = self.languages
            else:
                active_languages = languages

        if additional_languages:
            self._load_languages(additional_languages, is_additional=True)
            active_languages += additional_languages

        for language in active_languages:
            if not any(
                pattern in text
                for pattern in self.profanity_patterns.get(language).get(
                    "exclude_patterns", []
                )
                + custom_exclude_patterns
            ) and any(
                pattern in text
                for pattern in self.profanity_patterns.get(language).get("patterns", [])
                + custom_patterns
            ):
                return True
            return False

    def is_profane(
        self,
        word: str,
        languages: list[str] = None,
        additional_languages: list[str] = None,
        custom_patterns: list[str] = [],
        custom_exclude_patterns: list[str] = [],
    ) -> bool:
        """
        Checks if a given word is considered profane.

        Args:
            word (str): The word to check for profanity.
            languages (list[str], optional): List of languages to consider for profanity. Defaults to None.
            additional_languages (list[str], optional): Additional languages to consider for profanity. Defaults to None.
            custom_patterns (list[str], optional): Custom regex patterns to consider for profanity. Defaults to an empty list.
            custom_exclude_patterns (list[str], optional): Custom regex patterns to exclude from profanity check. Defaults to an empty list.

        Returns:
            bool: True if the word is considered profane, False otherwise.
        """

        return self.contains_profanity(
            word,
            languages,
            additional_languages,
            custom_patterns,
            custom_exclude_patterns,
        )

    def censor_word(
        self, word: str, partial_censor: bool = False, censoring_char: str = "#"
    ) -> str:
        """
        Censors a word either fully or partially.

        :param word: The word to censor.
        :param partial_censor: Whether to partially censor the word.
        :param censoring_char: The character to use for censorship.
        :return: The censored word.
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
        languages: list[str] = None,
        additional_languages: list[str] = None,
        custom_patterns: list[str] = [],
        custom_exclude_patterns: list[str] = [],
        partial_censor: bool = False,
        censor_symbol: str = "#",
    ) -> str:
        """
        Censors profanity in the given text based on specified languages and patterns.

        Args:
            text (str): The input text to be censored.
            languages (list[str], optional): List of languages to be used for censoring. If "all" is included, all available languages will be used. Defaults to None.
            additional_languages (list[str], optional): List of additional languages to be used for censoring. These are added to the primary languages. Defaults to None.
            custom_patterns (list[str], optional): List of custom patterns to be censored. Defaults to an empty list.
            custom_exclude_patterns (list[str], optional): List of custom patterns to be excluded from censoring. Defaults to an empty list.
            partial_censor (bool, optional): If True, partially censors the words. Defaults to False.
            censor_symbol (str, optional): The symbol used for censoring. Defaults to "#".

        Returns:
            str: The censored text.

        Examples:
            # Basic censoring with default settings
            >>> pf = ProfanityFilter()
            >>> pf.censor("This is a fucking bad word")
            'This is a ####### bad word'

            # Partial censoring
            >>> pf.censor("This is a fucking bad word", partial_censor=True)
            'This is a fu###ng bad word'

            # Custom censoring symbol
            >>> pf.censor("This is a fucking bad word", censor_symbol="*")
            'This is a ******* bad word'

            # Using specific languages
            >>> pf.censor("This is a bad word", languages=["uk"])
            'This is a піздєц bad word'

            # Using custom patterns
            >>> pf.censor("This is a custom bad word", custom_patterns=["custom"])
            'This is a ##### bad word'
        """
        active_languages = list(self.languages)  # Clone the current languages

        if languages:
            self._load_languages(languages)

            if "all" in languages:
                active_languages = self.languages
            else:
                active_languages = languages

        if additional_languages:
            self._load_languages(additional_languages, is_additional=True)
            active_languages += additional_languages

        lines = text.split("\n")

        censored_text = text

        for line in lines:
            words = line.split()

            profanity_patterns = set()
            exclude_patterns = set()

            for language in active_languages:
                profanity_patterns.update(self.profanity_patterns[language]["patterns"])
                exclude_patterns.update(
                    self.profanity_patterns[language]["exclude_patterns"]
                )

            profanity_patterns.update(custom_patterns)
            exclude_patterns.update(custom_exclude_patterns)

            for word in words:
                stripped_word = self._strip(word)
                normalized_word = self._normalize_word(word)

                if not any(
                    pattern in normalized_word for pattern in exclude_patterns
                ) and any(pattern in normalized_word for pattern in profanity_patterns):
                    censored_word = self.censor_word(
                        word=stripped_word,
                        partial_censor=partial_censor,
                        censoring_char=censor_symbol,
                    )
                    censored_text = censored_text.replace(
                        stripped_word,
                        censored_word,
                    )

        return censored_text
