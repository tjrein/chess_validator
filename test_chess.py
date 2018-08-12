import unittest
import chess

class TestChess(unittest.TestCase):

    def setUp(self):

        self.white = ["Rf1", "Ng5", "Kg1", "Pf2", "Ph3", "Pg3"]
        self.black = ["Kb8", "Ne8", "Pa7", "Pb7", "Pc7", "Ra5", "Qc6", "Bf4"]

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

    def run_movement_test(self, position, legal_moves):
        expected = chess.get_moves(position, self.value_map["chr_to_ind"], self.chess_board)
        actual = [self.translate_position(move) for move in legal_moves]

        self.assertItemsEqual(expected, actual) 

    def test_king_movement(self):
        self.run_movement_test("g1", ["h2"])

    def test_in_check(self):
        original_move = self.translate_position("g1")
        potential_move = self.translate_position("g2")

        self.assertTrue(chess.validate_check(original_move, potential_move, self.chess_board))


    def test_queen_movement(self):
        diagonal =  ["d5", "e4", "f3", "g2", "h1", "b5", "a4", "d7"]
        vertical = ["c1", "c2", "c3", "c4", "c5"] 
        horizontal = ["a6", "b6", "d6", "e6", "f6", "g6", "h6"]
        legal_moves = diagonal + vertical + horizontal

        self.run_movement_test("c6", legal_moves)

    def test_rook_movement(self):
        self.run_movement_test("a5", ["a1", "a2", "a3", "a4", "a6", "b5", "c5", "d5", "e5", "f5", "g5"])

    def test_knight_movement(self):
        self.run_movement_test("e8", ["d6", "f6", "g7"])

    def test_bishop_movement(self):
        self.run_movement_test("f4", ["g3", "g5", "e3", "d2", "c1", "e5", "d6"])

    def test_black_pawn_movement(self):
        self.run_movement_test("b7", ["b6"])

    def test_white_pawn_movement(self):
        self.run_movement_test("g3", ["g4", "f4"])


if __name__ == "__main__":
    unittest.main()
