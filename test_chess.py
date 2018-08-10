import unittest
import chess

class TestChess(unittest.TestCase):

    def setUp(self):
        self.white = ["Kg1"]
        self.black = ["Bf4", "Qc6"]
        self.chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]
        self.value_map = chess.generate_value_map()

    def helper_generate_value_map(self, test_dict, expected):
        return all(test_dict[i] == expected[i] for i in test_dict)

    def test_generate_value_map(self):
        expected_ind_to_num = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'} 
        expected_ind_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        expected_chr_to_ind = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
            '1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7 
        }
        
        assert self.helper_generate_value_map(self.value_map['ind_to_num'], expected_ind_to_num)
        assert self.helper_generate_value_map(self.value_map['ind_to_letter'], expected_ind_to_letter)
        assert self.helper_generate_value_map(self.value_map['chr_to_ind'], expected_chr_to_ind)


    def test_map_initial_values(self):
        values = self.value_map['chr_to_ind']
        chess.map_initial_values(self.white, self.black, values, self.chess_board)

        assert self.chess_board[0][6] == ('K', 'W')
        assert self.chess_board[3][5] == ('B', 'B')
        assert self.chess_board[5][2] == ('Q', 'B')

    def test_get_capture_patterns(self):
        pass

    def test_output_moves(self):
        pass

    def test_get_move_patterns(self):
        pass

    def test_is_inbounds(self):
        pass

    def test_fetch_chess_piece(self):
        pass

if __name__ == "__main__":
    unittest.main()
