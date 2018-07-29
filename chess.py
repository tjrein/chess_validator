def main(black=[], white=[], piece=None):
    white = ['Rf1', 'Kg1', 'Pf2', 'Ph2', 'Pg3', 'Bf5']
    black = ['Kb8', 'Be8', 'Pa7', 'Pb7', 'Pc7', 'Ra5']

    chess_board = [[0 for i in range(8)] for j in range(8)]
    value_map = generate_value_map()
    piece = 'Kb8'
    map_initial_values(white, black, value_map, chess_board)
    legal_moves = check_moves(piece[0:1], piece[1:], value_map, chess_board)
    output_moves(legal_moves, piece)

def map_initial_values(white, black, value_map, chess_board):
    for color in (black, white):
        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            indices = [value_map[i] for i in position]
            chess_board[indices[1]][indices[0]] = piece_type

def generate_value_map():
    value_map = {}

    for i in range(8):
        value_map[chr(97+i)] = i
        value_map[str(i+1)] = i

    return value_map

def output_moves(legal_moves, piece):
    numbers = {}
    letters = {}
    result = []

    for i in range(8):
        letters[i] = chr(97+i)
        numbers[i] = str(i+1)

    result = " ".join([letters[move[0]] + numbers[move[1]] for move in legal_moves])

    print "LEGAL MOVES FOR " + piece + ": " + result

def check_moves(piece_type, position, value_map, chess_board):
    legal_moves = []
    indices = [value_map[i] for i in position]
    moveset = get_moveset(piece_type, indices)

    for move in moveset:
        inbounds = 0 <= move[0] <= 7 and 0 <= move[1] <= 7 

        if inbounds and not chess_board[move[1]][move[0]]:
            legal_moves.append(move)

    return legal_moves

def get_moveset(piece_type, indices):
    i, j = indices

    return {
        "K": [[i-1, j+1], [i, j+1], [i+1, j+1], [i-1, j], [i+1, j], [i-1, j-1], [i, j-1], [i+1, j-1]]
    }[piece_type]

if __name__ == "__main__":
    main()
