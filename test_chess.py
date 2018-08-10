import unittest
import chess

class TestChess(unittest.TestCase):

    def setUp(self):
        self.white = ["Kg1", "Pg3"]
        self.black = ["Bf4", "Qc6", "Ph4"]
        self.chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]
        self.value_map = chess.generate_value_map()
        values = self.value_map['chr_to_ind']
        chess.map_initial_values(self.white, self.black, values, self.chess_board)

    def translate_position(self, position):
        values = self.value_map['chr_to_ind']
        letter, number = list(position)
        indices = [values[letter], values[number]]
        return indices

    def test_map_initial_values(self):
        self.assertEqual(self.chess_board[0][6], ('K', 'W'))
        self.assertEqual(self.chess_board[3][5], ('B', 'B'))
        self.assertEqual(self.chess_board[5][2], ('Q', 'B'))

    def test_in_check(self):
        original_move = self.translate_position("g1")
        potential_move = self.translate_position("g2")

        self.assertTrue(chess.validate_check(original_move, potential_move, self.chess_board))

    def test_not_in_check(self):
        original_move = self.translate_position("g1")
        potential_move = self.translate_position("f1")

        self.assertFalse(chess.validate_check(original_move, potential_move, self.chess_board))

    def run_movement_test(self, actual, expected):
        self.assertItemsEqual(actual, expected)

    def get_expected_moves(self, position):
        values = self.value_map['chr_to_ind']
        return chess.get_moves(position, values, self.chess_board)

    def get_actual_moves(self, positions):
        return [self.translate_position(position) for position in positions]
    
    def test_queen_movement(self):
        expected_moves = self.get_expected_moves("c6")
        actual_moves = self.get_actual_moves(["b7", "a8", "d5", "e4", "f3", "g2", "h1",
                                         "b5", "a4", "d7", "e8",
                                         "c1", "c2", "c3", "c4", "c5", "c7", "c8",
                                         "a6", "b6", "d6", "e6", "f6", "g6", "h6"])

        self.run_movement_test(actual_moves, expected_moves)


    def test_pawn_movement(self):
        expected_moves = chess.get_moves("h4", self.value_map["chr_to_ind"], self.chess_board)
        actual_moves = [ self.translate_position(position) for position in ("h3", "g3") ]

        self.run_movement_test(actual_moves, expected_moves)

if __name__ == "__main__":
    unittest.main()
