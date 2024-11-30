import unittest
from censore import ProfanityFilter
from censore.types import Text, Word


class TestProfanityFilter(unittest.TestCase):

    def setUp(self):
        self.filter = ProfanityFilter()

    # def test_contains_profanity(self):
    #     text_with_profanity = "This is a fucking bad text."
    #     text_without_profanity = "This is a very good text."
    #     self.assertTrue(
    #         self.filter.contains_profanity(text_with_profanity, languages=["en"])
    #     )
    #     self.assertFalse(
    #         self.filter.contains_profanity(text_without_profanity, languages=["en"])
    #     )

    def test_contains_profanity(self):
        profane_word = "fuck"
        non_profane_word = "good"
        self.assertTrue(self.filter.contains_profanity(profane_word, languages=["en"]))
        self.assertFalse(
            self.filter.contains_profanity(non_profane_word, languages=["en"])
        )

    def test_censor_word(self):
        word = "fuck"
        censored = self.filter.censor_word(word)
        self.assertEqual(
            Word(original=word, censored="####", is_profane=None), censored
        )

    def test_partial_censor_word(self):
        word = "fuck"
        partially_censored = self.filter.censor_word(word, partial_censor=True)
        self.assertEqual(
            Word(original=word, censored="f##k", is_profane=None), partially_censored
        )

    def test_censor(self):
        text = "This is a fucking bad text."
        censored = self.filter.censor(text, languages=["en"])
        self.assertIn("#######", censored.censored)
        self.assertNotIn("fucking", censored.censored)

    def test_add_custom_patterns(self):
        custom_patterns = ["foobar"]
        self.filter.add_custom_profanity_patterns(custom_patterns, [])
        self.assertTrue(
            self.filter.contains_profanity(
                "This is a foobar text.", languages=["custom"]
            )
        )

    def test_add_custom_lang(self):
        custom_patterns = ["foobar"]
        custom_exclude_patterns = ["notfoobar"]
        self.filter.add_custom_language(
            "custom_lang", custom_patterns, custom_exclude_patterns
        )
        self.assertTrue(
            self.filter.contains_profanity(
                "This is a foobar text.", languages=["custom_lang"]
            )
        )
        self.assertFalse(
            self.filter.contains_profanity(
                "This is a notfoobar text.", languages=["custom_lang"]
            )
        )

    def test_censor_special_characters(self):
        text = "It's @ssh0l3."
        censored = self.filter.censor(text, languages=["en"])
        self.assertEqual(
            Text(
                original=text,
                censored="It's #######.",
                is_profane=True,
                words_censored=1,
            ),
            censored,
        )


if __name__ == "__main__":
    unittest.main()
