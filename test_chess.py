import unittest
import chess

class TestChess(unittest.TestCase):
    def setUp(self):
        #simulate potential board configuration
        self.white = ["Rf1", "Ng5", "Kg1", "Pf2", "Ph3", "Pg3"]
        self.black = ["Kb8", "Ne8", "Pa7", "Pb7", "Pc7", "Ra5", "Qc6", "Bf4"]

        self.default_input_args = {
            'values': [],
            'move_piece': False,
            'cache': []
        }

        #place board configuration on board
        self.chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]
        self.value_map = chess.generate_value_map()
        values = self.value_map['chr_to_ind']
        chess.map_initial_values(self.white, self.black, values, self.chess_board)

    def test_sanitize_input(self):
        input_str = "    kG1,  Bf2 RG3   , qc6   "
        actual = ["Kg1", "Bf2", "Rg3", "Qc6"]

        self.assertItemsEqual(chess.sanitize_input(input_str), actual)

    def test_blank_input(self):
        self.run_input_test({})

    def test_too_many_values(self):
        self.run_input_test({'values': ['Kg1', 'Bg2'], 'move_piece': True})

    def test_piece_not_in_play(self):
        self.run_input_test({'values': ["Kg1"], 'move_piece': True, 'cache': ["g2"]})

    def test_piece_in_play(self):
        self.run_input_test({'values': ["Kg1"], 'move_piece': True, 'cache': ["g1"]}, fail=False)

    def test_invalid_input(self):
        self.run_input_test({'values': ['vgq']})

    def test_long_value(self):
        self.run_input_test({'values': ['Kg12']})

    def test_short_value(self):
        self.run_input_test({'values': ['kg']})

    def test_same_position_current(self):
        self.run_input_test({'values': ['Kg1', 'Bg1']})

    def test_same_position_previous(self):
        self.run_input_test({'values': ['Rf2'], 'cache': ['f2']})

    def test_valid_input(self):
        self.run_input_test({'values': ['Kg1', 'Bg2'], 'cache': ['Qc6']}, fail=False)

    def run_input_test(self, update_dict, fail=True):
        args = self.default_input_args

        for key, val in update_dict.iteritems():
            args[key] = val

        args_list = [args[i] for i in ['values', 'move_piece', 'cache']]
        result = chess.has_invalid_values(*args_list)
        method = self.assertTrue if fail else self.assertFalse
        method(result)

    def translate_position(self, position):
        values = self.value_map['chr_to_ind']
        letter, number = list(position)
        indices = [values[letter], values[number]]
        return indices

    def run_movement_test(self, piece, positions):
        origin = [self.value_map['chr_to_ind'][i] for i in piece[1:]]
        expected_moves = [self.translate_position(position) for position in positions]
        actual_moves = chess.get_moves(origin, self.chess_board)

        self.assertItemsEqual(expected_moves, actual_moves)
        self.compare_output(actual_moves, positions, piece)

    def compare_output(self, actual_moves, positions, piece):
        expected_string = " ".join(sorted(positions))
        expected_msg = "LEGAL MOVES FOR {0}: {1}".format(piece, expected_string)
        actual_msg = chess.format_moves(actual_moves, piece, self.value_map)

        self.assertEqual(expected_msg, actual_msg)

    def test_king_movement(self):
        self.run_movement_test("Kg1", ["h2"])

    def test_in_check(self):
        original_move = self.translate_position("g1")
        potential_move = self.translate_position("g2")

        self.assertTrue(chess.determine_check(original_move, potential_move, self.chess_board))

    def test_queen_movement(self):
        diagonal = ["d5", "e4", "f3", "g2", "h1", "b5", "a4", "d7"]
        vertical = ["c1", "c2", "c3", "c4", "c5"]
        horizontal = ["a6", "b6", "d6", "e6", "f6", "g6", "h6"]
        legal_moves = diagonal + vertical + horizontal

        self.run_movement_test("Qc6", legal_moves)

    def test_rook_movement(self):
        vertical = ["a1", "a2", "a3", "a4", "a6"]
        horizontal = ["b5", "c5", "d5", "e5", "f5", "g5"]

        self.run_movement_test("Ra5", vertical + horizontal)

    def test_knight_movement(self):
        self.run_movement_test("Ke8", ["d6", "f6", "g7"])

    def test_bishop_movement(self):
        self.run_movement_test("Bf4", ["g3", "g5", "e3", "d2", "c1", "e5", "d6"])

    def test_black_pawn_movement(self):
        self.run_movement_test("Pb7", ["b6"])

    def test_white_pawn_movement(self):
        self.run_movement_test("Pg3", ["g4", "f4"])

if __name__ == "__main__":
    unittest.main()
