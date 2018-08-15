from unittest import TestCase, main
from pydash import py_

from config import Locale, Theme
from field import Field
from ui import draw_field, make_ship_from_str


class DrawFieldTestCase(TestCase):
    def common(self, sample: str, *draw_args, **draw_kwargs) -> None:
        s = draw_field(*draw_args, **draw_kwargs)

        with open('./fixtures/{}.txt'.format(sample), 'r', encoding='utf8') as f:
            expected_lines = f.readlines()
            real_lines = s.split('\n')
            for expected, real in py_.zip_(expected_lines, real_lines):
                self.assertEqual(expected, real + '\n')

    def setUp(self) -> None:
        self.field = Field(fleet=[
            [(1, 1), (1, 2), (1, 3), (1, 4)]
        ], player_name='player_name')
        self.field.hit((0, 0))
        self.field.hit((1, 0))
        self.field.hit((0, 1))
        self.field.hit((1, 2))

    def test_player_numbers_right(self) -> None:
        self.common('field_player_numbers_right',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=True, opponent=False)

    def test_player_numbers_left(self) -> None:
        self.common('field_player_numbers_left',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=False, opponent=False)

    def test_opponent_numbers_right(self) -> None:
        self.common('field_opponent_numbers_right',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=True, opponent=True)

    def test_opponent_numbers_left(self) -> None:
        self.common('field_opponent_numbers_left',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=False, opponent=True)

    def test_player_numbers_right_border(self) -> None:
        self.common('field_player_numbers_right_border',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=True, opponent=False, border=True)

    def test_player_numbers_left_border(self) -> None:
        self.common('field_player_numbers_left_border',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=False, opponent=False, border=True)

    def test_opponent_numbers_right_border(self) -> None:
        self.common('field_opponent_numbers_right_border',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=True, opponent=True, border=True)

    def test_opponent_numbers_left_border(self) -> None:
        self.common('field_opponent_numbers_left_border',
                    self.field, Locale.RU, Theme.MAIN, numbers_right=False, opponent=True, border=True)


class MakeShipFromStrTestCase(TestCase):
    def test_horizontal_ru(self) -> None:
        self.assertEqual(
            make_ship_from_str("Г1Е1", Locale.RU),
            [(0, 3), (0, 4), (0, 5)]
        )

    def test_horizontal_ru_2deck(self) -> None:
        self.assertEqual(
            make_ship_from_str("Г1Д1", Locale.RU),
            [(0, 3), (0, 4)]
        )

    def test_vertical_ru(self) -> None:
        self.assertEqual(
            make_ship_from_str("Г1Г4", Locale.RU),
            [(0, 3), (1, 3), (2, 3), (3, 3)]
        )

    def test_vertical_ru_upper_left(self) -> None:
        self.assertEqual(
            make_ship_from_str("А1А4", Locale.RU),
            [(0, 0), (1, 0), (2, 0), (3, 0)]
        )

    def test_diagonal_ru(self) -> None:
        with self.assertRaises(Exception) as ctx:
            make_ship_from_str("Г1Д2", Locale.RU)

        self.assertEqual(ctx.exception.args[0], 'Ship should be a straight line')

    def test_single_ru(self) -> None:
        self.assertEqual(
            make_ship_from_str("Г1", Locale.RU),
            [(0, 3)]
        )

    def test_horizontal_en(self) -> None:
        self.assertEqual(
            make_ship_from_str("D1F1", Locale.EN),
            [(0, 3), (0, 4), (0, 5)]
        )

    def test_incorrect_ru(self) -> None:
        with self.assertRaises(AssertionError) as ctx:
            make_ship_from_str("Г1Г2Г3", Locale.RU)

        self.assertEqual(ctx.exception.args[0], 'Incorrect input')

    def test_incorrect_locale(self) -> None:
        with self.assertRaises(AssertionError) as ctx:
            make_ship_from_str("Г1Г2", Locale.EN)

        self.assertEqual(ctx.exception.args[0], 'Incorrect input')

    def test_10(self) -> None:
        self.assertEqual(
            make_ship_from_str("А10Г10", Locale.RU),
            [(9, 0), (9, 1), (9, 2), (9, 3)]
        )

    def test_out_of_bounds(self) -> None:
        with self.assertRaises(Exception):
            make_ship_from_str("Г10Г12", Locale.RU)

    def test_out_of_bounds_2(self) -> None:
        with self.assertRaises(Exception):
            make_ship_from_str("А9А11", Locale.RU)


if __name__ == '__main__':
    main()
