import unittest
import chess

class TestChess(unittest.TestCase):

    def setUp(self):
        self.white = ["Kg1"]
        self.black = ["Bf4", "Qc6"]
        self.chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]
        self.value_map = chess.generate_value_map()
        values = self.value_map['chr_to_ind']
        chess.map_initial_values(self.white, self.black, values, self.chess_board)

    def test_map_initial_values(self):
        self.assertEqual(self.chess_board[0][6], ('K', 'W'))
        self.assertEqual(self.chess_board[3][5], ('B', 'B'))
        self.assertEqual(self.chess_board[5][2], ('Q', 'B'))

    def test_validate_check(self):
        self.assertFalse(chess.validate_check([6,0], [5, 0], self.chess_board))
        self.assertTrue(chess.validate_check([6,0], [6, 1], self.chess_board))


    def test_get_move_patterns(self):
        pass

    def test_is_inbounds(self):
        pass

    def test_fetch_chess_piece(self):
        pass

if __name__ == "__main__":
    unittest.main()
