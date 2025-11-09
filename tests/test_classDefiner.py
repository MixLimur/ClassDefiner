import unittest
from classDefiner import asDictionaryItem, getParameters


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
class TestClassDefiner(unittest.TestCase):
    def test_DictionaryItem(self):
        asDictionaryItem("age[0:100] +s +g -re = 20")
        self.assertTrue(True)

    def test_getParameters(self):
        params = {
        "setter": False,
        "getter": False,
        "exception": True
        }
        self.assertDictEqual(getParameters("-s   -g + e"), params)

        params = {
            "setter": False,
            "getter": True,
            "exception": True
        }
        self.assertDictEqual(getParameters("-s +g +e "), params)

        params = {
            "setter": True,
            "getter": True,
            "exception": False
        }
        self.assertDictEqual(getParameters(""), params)

        params = {
            "setter": False,
            "getter": True,
            "exception": False
        }
        self.assertDictEqual(getParameters("-s-e"), params)


if __name__ == '__main__':
    unittest.main()
