import unittest
import check_field
from configs.cell_state import CellState


class FieldValidatorTestCase(unittest.TestCase):

    def test_cell_state(self):
        self.assertEqual(CellState.CELL_DECK.value, 2)
        self.assertEqual(CellState.CELL_EMPTY.value, 1)
        self.assertEqual(CellState.CELL_FOG.value, 0)

    def test_find_checked_coords(self):
        field = [
            [1, 2, 2, 1],
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [1, 1, 1, 1],
        ]
        self.assertEqual(
            check_field.find_checked_coords(field), [(0, 1), (0, 2), (2, 0), (2, 1), (2, 2), (2, 3)]
        )

    def test_find_ships(self):
        field = [
            [1, 2, 2, 1, 1],
            [1, 1, 1, 1, 2],
            [2, 2, 2, 2, 1],
            [1, 1, 2, 1, 1],
            [1, 1, 1, 1, 2],
        ]
        self.assertEqual(
            check_field.find_ships(field), [
                [(0, 1), (0, 2)],
                [(1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 2)],
                [(4, 4)]
            ]
        )

    def test_find_adjacent_cells(self):
        cells = [(2, 2), (2, 3), (2, 1), (1, 2), (3, 2), (3, 3), (0, 0)]
        self.assertEqual(check_field.find_adjacent_cells(cells[0], cells), [
            (2, 3), (2, 1), (1, 2), (3, 2), (3, 3)
        ])

    def test_check_ship_shape(self):
        ships = [
            [(1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 2)],
            [(0, 1), (0, 2)],
            [(4, 4)]
        ]
        tests = list(map(check_field.check_ship_shape, ships))
        self.assertEqual(tests, [False, True, True])


class FieldValidator(unittest.TestCase):
    def test_validate_field_ok(self):
        FIELD_OK = [
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
        self.assertTrue(check_field.validate_field(FIELD_OK))

    def test_validate_field_colliding_ships(self):
        FIELD_COLLIDING_SHIPS = [
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
            check_field.validate_field(FIELD_COLLIDING_SHIPS)

        self.assertEqual(ctx.exception.args[0], 'Fleet config is invalid (ships are touching or extra/missing ship)')

    def test_validate_field_wrong_shape(self):
        FIELD_WRONG_SHAPE = [
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
            check_field.validate_field(FIELD_WRONG_SHAPE)

        self.assertEqual(ctx.exception.args[0],
                         'There is a deformed ship somewhere on the field ([(1, 6), (2, 4), (2, 5), (2, 6)])')

    def test_validate_field_extra_ship(self):
        FIELD_EXTRA_SHIP = [
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
            check_field.validate_field(FIELD_EXTRA_SHIP)

        self.assertEqual(ctx.exception.args[0], 'Fleet config is invalid (ships are touching or extra/missing ship)')

    def test_validate_field_out_of_bounds(self):
        FIELD_SHIP_OUTSIDE_BOUNDS = [
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
            check_field.validate_field(FIELD_SHIP_OUTSIDE_BOUNDS)

        self.assertEqual(ctx.exception.args[0],
                         'Ship outside bounds ([(10, 1)])')


class FleetConfigValidator(unittest.TestCase):
    def test_check_fleet_config_ok(self):
        self.assertTrue(check_field.check_fleet_config([
            [1, 2, 3, 4],
            [1, 2, 3], [1, 2, 3],
            [1, 2], [1, 2], [1, 2],
            [1], [1], [1], [1],
        ]))

    def test_check_fleet_config_extra_ship(self):
        self.assertFalse(check_field.check_fleet_config([
            [1, 2, 3, 4], [1, 2, 3, 4],
            [1, 2, 3], [1, 2, 3],
            [1, 2], [1, 2], [1, 2],
            [1], [1], [1], [1],
        ]))

    def test_check_fleet_config_missing_ship(self):
        self.assertFalse(check_field.check_fleet_config([
            [1, 2, 3], [1, 2, 3],
            [1, 2], [1, 2], [1, 2],
            [1], [1], [1], [1],
        ]))

    def test_check_fleet_config_setup_stage_missing_all_ships_of_type(self):
        self.assertEqual(
            check_field.check_fleet_config([
                [1, 2, 3], [1, 2, 3],
                [1, 2], [1, 2], [1, 2],
                [1], [1], [1], [1],
            ], is_setup_stage=True),
            (False, {4:1, 3:0, 2:0, 1:0})
        )

    def test_check_fleet_config_setup_stage_missing_ship(self):
        self.assertEqual(
            check_field.check_fleet_config([
                [1, 2, 3, 4],
                [1, 2, 3], [1, 2, 3],
                [1, 2], [1, 2], [1, 2],
                [1], [1], [1],
            ], is_setup_stage=True),
            (False, {4: 0, 3: 0, 2: 0, 1: 1})
        )

if __name__ == '__main__':
    unittest.main()
