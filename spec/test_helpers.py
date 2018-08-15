from unittest import TestCase, main
from helpers import zip_by_keys


class MyTestCase(TestCase):
    def test_zip_by_keys(self) -> None:
        dicts = [
            {"a": 1, "b": 2, "c": 3},
            {"a": 10, "b": 20, "c": 30},
            {"a": 100, "b": 200, "c": 300}
        ]
        expected = {
            "a": [1, 10, 100],
            "b": [2, 20, 200],
            "c": [3, 30, 300]
        }
        self.assertEqual(
            zip_by_keys(dicts),
            expected
        )

    def test_uneven(self) -> None:
        dicts = [
            {"a": 1, "b": 2},
            {"a": 10, "c": 30},
            {"b": 200, "c": 300}
        ]
        expected = {
            "a": [1, 10, None],
            "b": [2, None, 200],
            "c": [None, 30, 300]
        }
        self.assertEqual(
            zip_by_keys(dicts),
            expected
        )


if __name__ == '__main__':
    main()
