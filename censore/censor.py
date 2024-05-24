import os
from typing import List, Dict, Optional


class Censor:
    def __init__(
        self, languages: List[str] = ["en"], custom_words: Optional[List[str]] = None
    ) -> None:
        """
        Initializes the Censor object by loading the appropriate profanity lists
        for the specified languages.

        :param languages: List of languages to load for censorship. If "all", loads all available languages.
        """
        self.languages: List[str] = []
        self.profanity_list: Dict[str, List[str]] = {}
        self.data_folder = os.path.join(os.path.dirname(__file__), "data/list")

        # Substitution table for normalizing words
        self.substitution_table = str.maketrans(
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

        # Load profanity lists for each language
        self._load_languages(languages)

        if custom_words:
            self.add_custom_words(custom_words)

    def _load_languages(
        self, languages: List[str], is_additional: bool = False
    ) -> None:
        """
        Loads the list of profane words for the specified language(s) from files.

        :param languages: A list of languages to load for censorship. If "all", loads all available languages.
        :return: None
        """
        languages_for_loading = []

        # Load languages
        if "all" in languages:
            for filename in os.listdir(self.data_folder):
                if filename.endswith(".txt"):
                    languages_for_loading.append(os.path.splitext(filename)[0])
        else:
            languages_for_loading = languages

        for language in languages_for_loading:
            self._load_language(language, is_additional)

    def _load_language(self, language: str, is_additional: bool = False) -> None:
        """
        Loads the list of profane words for the specified language from a file.

        :param language: The language for which to load the profanity list.
        """

        if language not in self.languages:
            path_to_list = os.path.join(self.data_folder, f"{language}.txt")

            with open(path_to_list, "r", encoding="utf-8") as file:
                profanities = file.read().split()

            self.profanity_list[language] = profanities

            if not is_additional:
                self.languages.append(language)

    def add_custom_words(
        self, custom_words: List[str], language: str = "custom"
    ) -> None:
        """
        Adds custom words to the profanity list.

        :param custom_words: A list of custom words to add to the profanity list.
        """

        self.add_custom_lang(language, custom_words)

    def add_custom_lang(self, language: str, custom_words: List[str]) -> None:
        """
        Adds custom words to the profanity list for the specified language.

        :param language: The language for which to add the custom words.
        :param custom_words: A list of custom words to add to the profanity list for the specified language.
        """

        if language not in self.profanity_list:
            self.profanity_list[language] = []

        self.profanity_list[language] = custom_words

        if language not in self.languages:
            self.languages.append(language)

    def _normalize_word(self, word: str) -> str:
        """
        Normalizes a word by substituting characters according to the substitution table
        and removing punctuation.

        :param word: The word to normalize.
        :return: The normalized word.
        """
        return self._strip(word.translate(self.substitution_table)).lower()

    def _strip(self, word: str) -> str:
        """
        Strips punctuation from the beginning and end of a word.

        :param word: The word to strip.
        :return: The stripped word.
        """
        return word.strip(".,!?:;/()[]{}-")

    def contains_profanity(
        self, text: str, languages: Optional[List[str]] = None
    ) -> bool:
        """
        Checks if the input string contains any profanity from the specified languages.

        :param text: The input string to check for profanity.
        :param languages: A list of languages to check for profanity. If "all", checks all available languages.
        :return: True if the string contains profanity, False otherwise.
        """

        lines = text.split("\n")

        # Ensure all specified languages are loaded
        if languages:
            self._load_languages(languages)

            if "all" in languages:
                languages = self.languages
        else:
            languages = self.languages

        for line in lines:
            words = line.split(" ")

            for language in languages:
                for word in words:
                    normalized_word = self._normalize_word(word)

                    if normalized_word in self.profanity_list.get(language, []):
                        return True

        return False

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
            if len(word) > 4:
                return word[:2] + censoring_char * (len(word) - 4) + word[-2:]
            else:
                return censoring_char * len(word)
        else:
            return censoring_char * len(word)

    def censor_text(
        self,
        text: str,
        languages: Optional[List[str]] = None,
        additional_languages: Optional[List[str]] = None,
        custom_words: List[str] = [],
        partial_censor: bool = False,
        censoring_char: str = "#",
    ) -> str:
        """
        Censors an entire text, replacing profane words according to the specified languages.

        :param text: The text to censor.
        :param languages: The list of languages to use for censorship.
        :param partial_censor: Whether to partially censor the words.
        :param censoring_char: The character to use for censorship.
        :return: The censored text.
        """

        lines = text.split("\n")
        censored_lines = []

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

        for line in lines:
            words = line.split(" ")

            for language in active_languages:
                for i, word in enumerate(words):
                    normalized_word = self._normalize_word(word)

                    if (
                        normalized_word in self.profanity_list.get(language, [])
                        or normalized_word in custom_words
                    ):
                        words[i] = words[i].replace(
                            self._strip(word),
                            self.censor_word(
                                self._strip(word), partial_censor, censoring_char
                            ),
                        )

            censored_line = " ".join(words)
            censored_lines.append(censored_line)

        return "\n".join(censored_lines)
