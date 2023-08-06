import unittest
from simplepythonwer.simplepythonwer import wer, ler


class TestWERMethod(unittest.TestCase):

    # -1. empty ground-truth -
    def test_empty_gt(self):
        # self.assertRaises(ZeroDivisionError, lambda :wer('  ', ' cat sat '))
        # if gt has at least some char then
        self.assertEqual(wer('  ', ' cat sat '), 2.0)
        self.assertEqual(wer('', ' cat sat '), 2.0)

    # 0. empty str
    def test_string_empty_asr(self):
        # if gt has at least some char then
        self.assertEqual(wer(" _ ", " "), 1.0)
        self.assertEqual(wer(" _ ", " "*5), 1.0)

    # 1. string equal
    # if both arguments are the same the WER should be 0
    def test_string_equality(self):
        self.assertEqual(wer("the cat", "the cat"), 0)

    # 2. As with 1 but with whitespace
    # whitespace shouldn't make a difference to the WER (if the word count is equal)
    def test_string_equality_whitespace(self):
        self.assertEqual(wer("the cat", " the   cat "), 0)

    # 3. two wrong words in 4 should be 0.5 wer
    def test_2_wrong_words(self):
        self.assertEqual(wer("the cat sat on", "my dog sat on"), 0.5)

    # 4. having a longer res > ground truth should result in > 1.0 WER
    def test_longer_res(self):
        self.assertGreater(wer("cat", "the cat sat on"), 1.0)

    # 5. unicode and emoji should work - and not error
    def test_unicode(self):
        test_wer = wer("my cat sat on the mat", "Meine Katze saß auf der Matte")
        self.assertIsInstance(test_wer, float)
        test_wer = wer("Meine Katze saß auf der Matte", "Meine Katze saß auf der Matte")
        self.assertEqual(test_wer, 0.0)
        test_wer = wer("🎉 🎉 🎉", "🎉 🎉 🎉")
        self.assertEqual(test_wer, 0.0)
        test_wer = wer("🎉 🎉 🎉 🎉", "🎉 🎉 ")
        self.assertEqual(test_wer, 0.5)

    # 6. doing WER on non-str should fail
    def test_nonstr_fails(self):
        self.assertRaises(AttributeError, lambda :wer(['123',123], ['']))
        self.assertRaises(AttributeError, lambda :wer(123, 123))
        self.assertRaises(AttributeError, lambda :wer('123', 123))
        self.assertRaises(AttributeError, lambda :wer(123, "123"))
        self.assertRaises(AttributeError, lambda :wer(10.5, "123"))

    # 7. similar to #4. if result is empty or completely wrong, the WER will always be 1.0
    def test_wer_values(self):
        test_cases = ['the', 'cat sat', 'on the matt']
        for test in test_cases:
            self.assertEqual(wer(test, ''), 1.0)

    # 8. ler is identical to wer without the split
    def test_ler_values(self):
        z = 'the cat sat on the matt'
        x=wer(z, z)
        y=ler(z.split(), z.split())
        self.assertEqual(x,y)

        x=wer(z, z[::-1])
        y=ler(z.split(), z[::-1].split())
        self.assertEqual(x,y)

# running the tests - use: PYTHONPATH=$(pwd) python3 -m unittest discover .
