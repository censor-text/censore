from unittest import TestCase, main
from censore import Censor


class TestCensor(TestCase):
    def test_normalize_word(self):
        self.assertEqual(Censor._normalize_word("h3ll0!"), "hello")

    def test_strip(self):
        self.assertEqual(Censor._strip("?hello?"), "hello")

    def test_contains_profanity(self):
        self.assertTrue(
            Censor().contains_profanity("lorem ipsum @ssh0l3 dolor sit amet")
        )

    def test_is_profane(self):
        self.assertTrue(Censor().is_profane("fuck3r"))

    def test_censor_word(self):
        self.assertEqual(Censor().censor_word("@ssh0l3"), "#######")

    def test_censor_text(self):
        self.assertEqual(Censor().censor_text("@ssh0l3 and d1ck"), "####### and ####")


if __name__ == "__main__":
    main()
