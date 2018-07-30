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

    result = " ".join(sorted([letters[move[0]] + numbers[move[1]] for move in legal_moves]))

    print "LEGAL MOVES FOR " + piece + ": " + result

def check_moves(piece_type, position, value_map, chess_board):
    legal_moves = []
    indices = [value_map[i] for i in position]
    moveset = get_moveset(piece_type, indices, chess_board)

    for move in moveset:
        inbounds = 0 <= move[0] <= 7 and 0 <= move[1] <= 7 

        if inbounds and not chess_board[move[1]][move[0]]:
            legal_moves.append(move)

    return legal_moves

def get_deterministic_moves(move_patterns, indices):
    potential_moves = []
    i, j = indices

    for pattern in move_patterns:
        p0, p1 = pattern
        potential_move = [i+p0, j+p1]
        potential_moves.append(potential_move)

    return potential_moves

def get_indeterministic_moves(move_patterns, indices, chess_board):
    i, j = indices
    potential_moves = []

    for pattern in move_patterns:
        p0, p1 = pattern
        potential_move = [i+p0, j+p1]
        inbounds = True
        obstructed = False

        while inbounds and not obstructed:
            k, l = potential_move
            inbounds = 0 <= k <= 7 and 0 <= l <= 7
            obstructed = inbounds and chess_board[l][k]  

            if inbounds and not obstructed:
                potential_moves.append(potential_move)
                potential_move = [k+p0, l+p1]

    return potential_moves

def get_moveset(piece_type, indices, chess_board):
    diagonal_movement = [[1, 1], [1, -1], [-1, +1], [-1, -1]]
    xy_movement = [[-1, 0], [1, 0], [0, 1], [0, -1]] 

    move_patterns = {
        "K": [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]],
        "N": [[-2, 1], [-1, 2], [1, 2], [2, 1], [-2, -1], [-1, -2], [2, -1], [1, -2]],
        "B": diagonal_movement,
        "R": xy_movement,
        "Q": diagonal_movement + xy_movement,
    }[piece_type]

    if piece_type in ["K", "N"]:
        return get_deterministic_moves(move_patterns, indices)

    if piece_type in ["B", "Q", "R"]:
        return get_indeterministic_moves(move_patterns, indices, chess_board)

if __name__ == "__main__":
    main()
