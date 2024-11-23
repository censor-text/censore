import unittest
from censore import ProfanityFilter


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
        censored_word = self.filter.censor_word(word)
        self.assertEqual(censored_word, "####")

    def test_partial_censor_word(self):
        word = "fuck"
        partially_censored_word = self.filter.censor_word(word, partial_censor=True)
        self.assertEqual(partially_censored_word, "f##k")

    def test_censor(self):
        text = "This is a fucking bad text."
        censored_text = self.filter.censor(text, languages=["en"])
        self.assertIn("#######", censored_text)
        self.assertNotIn("fucking", censored_text)

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
        censored_text = self.filter.censor(text, languages=["en"])
        self.assertEqual("It's #######.", censored_text)


if __name__ == "__main__":
    unittest.main()
