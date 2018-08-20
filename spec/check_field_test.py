from unittest import TestCase

from check_field import find_checked_cells, find_ships, find_adjacent_cells, \
    validate_field, check_ship_shape, check_fleet_config, get_available_cells, \
    find_straight_segments
from config import CellState
from Coord import Coord
import pydash as py_


class FieldValidatorTestCase(TestCase):

    def test_cell_state(self) -> None:
        self.assertEqual(CellState.CELL_DECK.value, 2)
        self.assertEqual(CellState.CELL_EMPTY.value, 1)
        self.assertEqual(CellState.CELL_FOG.value, 0)

    def test_find_checked_cells(self) -> None:
        field = [
            [1, 2, 2, 1],
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [1, 1, 1, 1],
        ]
        self.assertEqual(
            find_checked_cells(field),
            [Coord((0, 1)), Coord((0, 2)), Coord((2, 0)), Coord((2, 1)), Coord((2, 2)), Coord((2, 3))]
        )

    def test_find_ships(self) -> None:
        field = [
            [1, 2, 2, 1, 1],
            [1, 1, 1, 1, 2],
            [2, 2, 2, 2, 1],
            [1, 1, 2, 1, 1],
            [1, 1, 1, 1, 2],
        ]
        self.assertEqual(
            find_ships(field), [
                [Coord((0, 1)), Coord((0, 2))],
                [Coord((1, 4)), Coord((2, 0)), Coord((2, 1)), Coord((2, 2)), Coord((2, 3)), Coord((3, 2))],
                [Coord((4, 4))]
            ]
        )

    def test_find_adjacent_cells(self) -> None:
        cells = py_.map_([(2, 2), (2, 3), (2, 1), (1, 2), (3, 2), (3, 3), (0, 0)], Coord)
        self.assertEqual(find_adjacent_cells(cells[0], cells), py_.map_([
            (2, 3), (2, 1), (1, 2), (3, 2), (3, 3)
        ], Coord))

    def test_check_ship_shape(self) -> None:
        ships = [
            [Coord((1, 4)), Coord((2, 0)), Coord((2, 1)), Coord((2, 2)), Coord((2, 3)), Coord((3, 2))],
            [Coord((0, 1)), Coord((0, 2))],
            [Coord((4, 4))]
        ]
        tests = list(map(check_ship_shape, ships))
        self.assertEqual(tests, [False, True, True])


class FieldValidator(TestCase):
    def test_validate_field_ok(self) -> None:
        field_ok = [
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 2, 1, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.assertTrue(validate_field(field_ok))

    def test_validate_field_colliding_ships(self) -> None:
        field_colliding_ships = [
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 1, 2, 1, 2, 2, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        with self.assertRaises(Exception) as ctx:
            validate_field(field_colliding_ships)

        self.assertEqual(ctx.exception.args[0], 'Fleet config is invalid (ships are touching or extra/missing ship)')

    def test_validate_field_wrong_shape(self) -> None:
        field_wrong_shape = [
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 2, 1, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        with self.assertRaises(Exception) as ctx:
            validate_field(field_wrong_shape)

        self.assertEqual(ctx.exception.args[0],
                         'There is a deformed ship somewhere on the field '
                         '([Coord.Coord((1,6)), Coord.Coord((2,4)), Coord.Coord((2,5)), '
                         'Coord.Coord((2,6))])')

    def test_validate_field_extra_ship(self) -> None:
        field_extra_ship = [
            [1, 2, 1, 1, 1, 2, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 2, 1, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        with self.assertRaises(Exception) as ctx:
            validate_field(field_extra_ship)

        self.assertEqual(ctx.exception.args[0], 'Fleet config is invalid (ships are touching or extra/missing ship)')

    def test_validate_field_out_of_bounds(self) -> None:
        field_ship_outside_bounds = [
            [1, 2, 1, 1, 1, 2, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 2, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        with self.assertRaises(Exception) as ctx:
            validate_field(field_ship_outside_bounds)

        self.assertEqual(ctx.exception.args[0],
                         'Ship outside bounds ([Coord.Coord((10,1))])')


class FleetConfigValidator(TestCase):
    def test_check_fleet_config_ok(self) -> None:
        self.assertTrue(check_fleet_config([
            [1, 2, 3, 4],
            [1, 2, 3], [1, 2, 3],
            [1, 2], [1, 2], [1, 2],
            [1], [1], [1], [1],
        ]))

    def test_check_fleet_config_extra_ship(self) -> None:
        self.assertEqual(
            (False, None),
            check_fleet_config([
                [1, 2, 3, 4], [1, 2, 3, 4],
                [1, 2, 3], [1, 2, 3],
                [1, 2], [1, 2], [1, 2],
                [1], [1], [1], [1],
            ])
        )

    def test_check_fleet_config_missing_ship(self) -> None:
        self.assertEqual(
            (False, {4: 1}),
            check_fleet_config([
                [1, 2, 3], [1, 2, 3],
                [1, 2], [1, 2], [1, 2],
                [1], [1], [1], [1],
            ])
        )

    def test_check_fleet_config_setup_stage_missing_all_ships_of_type(self) -> None:
        self.assertEqual(
            (True, {4: 1}),
            check_fleet_config([
                [1, 2, 3], [1, 2, 3],
                [1, 2], [1, 2], [1, 2],
                [1], [1], [1], [1],
            ], is_setup_stage=True)
        )

    def test_check_fleet_config_setup_stage_missing_ship(self) -> None:
        self.assertEqual(
            (True, {1: 1}),
            check_fleet_config([
                [1, 2, 3, 4],
                [1, 2, 3], [1, 2, 3],
                [1, 2], [1, 2], [1, 2],
                [1], [1], [1],
            ], is_setup_stage=True),
        )

    def test_check_fleet_config_setup_stage_extra_ship(self) -> None:
        self.assertEqual(
            (False, None),
            check_fleet_config([
                [1, 2, 3, 4], [1, 2, 3, 4],
                [1, 2, 3], [1, 2, 3],
                [1, 2], [1, 2], [1, 2],
                [1], [1], [1],
            ], is_setup_stage=True)
        )


class GetAvailableCellsValidator(TestCase):
    def test_basic(self) -> None:
        c = CellState.CELL_DECK.value
        field = [
            [0, 0, 0, 0],
            [0, c, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(
            [
                Coord((0, 3)), Coord((1, 3)), Coord((2, 3)),
                Coord((3, 0)), Coord((3, 1)), Coord((3, 2)), Coord((3, 3))
            ],
            sorted(get_available_cells(field, Coord((4, 4))))
        )

    def test_bigger_field(self) -> None:
        c = CellState.CELL_DECK.value
        field = [
            [0, 0, 0, 0, 0, 0],
            [0, c, 0, 0, 0, 0],
            [0, 0, 0, 0, c, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.assertEqual(
            py_.map_([
                (0, 3), (0, 4), (0, 5),
                (3, 0), (3, 1), (3, 2)
            ], Coord),
            sorted(get_available_cells(field, Coord((4, 6))))
        )


class FindStraightSegmentsValidator(TestCase):
    def test_singular(self) -> None:
        c = CellState.CELL_DECK.value
        field = [
            [0, 0, 0, 0],
            [0, c, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(
            [
                [Coord((0, 3))],
                [Coord((1, 3))],
                [Coord((2, 3))],
                [Coord((3, 0)), Coord((3, 1)), Coord((3, 2)), Coord((3, 3))]
            ],
            find_straight_segments(get_available_cells(field, Coord((4, 4))))
        )

    def test_singular_vertical(self) -> None:
        c = CellState.CELL_DECK.value
        field = [
            [0, 0, 0, 0],
            [0, c, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(
            [
                [Coord((0, 3)), Coord((1, 3)), Coord((2, 3)), Coord((3, 3))],
                [Coord((3, 0))],
                [Coord((3, 1))],
                [Coord((3, 2))]
            ],
            find_straight_segments(
                get_available_cells(field, Coord((4, 4))),
                vertical=True
            )
        )
