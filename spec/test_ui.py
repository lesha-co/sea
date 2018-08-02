import unittest
import pydash as _
from configs.locale import Locale
from configs.theme import Theme
from field import Field
from ui import draw_field


class DrawFieldTestCase(unittest.TestCase):

    def setUp(self):
        self.field = Field(fleet=[
            [(1, 1), (1, 2), (1, 3), (1, 4)]
        ]).hit((0, 0)).hit((1, 0)).hit((0, 1)).hit((1, 2))

    def test_player_numbers_right(self):

        s = draw_field(self.field, Locale.RU, Theme.MAIN, numbers_right=True, opponent=False)

        with open('./fixtures/field_player_numbers_right.txt', 'r', encoding='utf8') as f:
            expected_lines = f.readlines()
            real_lines = s.split('\n')
            for expected, real in _.zip_(expected_lines, real_lines):
                self.assertEqual(expected, real+'\n')

    def test_player_numbers_left(self):

        s = draw_field(self.field, Locale.RU, Theme.MAIN, numbers_right=False, opponent=False)

        with open('./fixtures/field_player_numbers_left.txt', 'r', encoding='utf8') as f:
            expected_lines = f.readlines()
            real_lines = s.split('\n')
            for expected, real in _.zip_(expected_lines, real_lines):
                self.assertEqual(expected, real+'\n')

    def test_opponent_numbers_right(self):

        s = draw_field(self.field, Locale.RU, Theme.MAIN, numbers_right=True, opponent=True)

        with open('./fixtures/field_opponent_numbers_right.txt', 'r', encoding='utf8') as f:
            expected_lines = f.readlines()
            real_lines = s.split('\n')
            for expected, real in _.zip_(expected_lines, real_lines):
                self.assertEqual(expected, real+'\n')

    def test_opponent_numbers_left(self):

        s = draw_field(self.field, Locale.RU, Theme.MAIN, numbers_right=False, opponent=True)

        with open('./fixtures/field_opponent_numbers_left.txt', 'r', encoding='utf8') as f:
            expected_lines = f.readlines()
            real_lines = s.split('\n')
            for expected, real in _.zip_(expected_lines, real_lines):
                self.assertEqual(expected, real+'\n')


if __name__ == '__main__':
    unittest.main()
