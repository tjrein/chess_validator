def main(black=[], white=[], piece=None):
    chess_board = [[0 for i in range(8)] for j in range(8)]
    value_map = generate_value_map()
    white = ['Rf1', 'Kg1', 'Pf2', 'Ph2', 'Pg3', 'Bf5']
    black = ['Kb8', 'Ne8', 'Pa7', 'Pb7', 'Pc7', 'Ra5']
    map_values(white, black, value_map, chess_board)

def map_values(white, black, value_map, chess_board):
    for played_piece in white:
        piece_type = played_piece[0:1]
        position = played_piece[1:]
        place_piece(piece_type, position, chess_board, value_map)

def place_piece(piece_type, position, chess_board, value_map):
    indices = [value_map[i] for i in position]
    chess_board[indices[1]][indices[0]] = piece_type
    print chess_board

def generate_value_map():
    value_map = {}

    for i in range(8):
        value_map[chr(97+i)] = i
        value_map[str(i+1)] = i

    return value_map
    
            


if __name__ == "__main__":
    main()
