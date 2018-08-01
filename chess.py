def main(black=[], white=[], piece=None):
    white = ['Rf1', 'Kg1', 'Bf2', 'Ph2', 'Pg3', 'Bf5']
    black = ['Kb8', 'Qe8', 'Pa7', 'Pb7', 'Pc7', 'Ra5']

    chess_board = [[0 for i in range(8)] for j in range(8)]
    value_map = generate_value_map()
    piece = 'Kg1'
    map_initial_values(white, black, value_map, chess_board)
    legal_moves = get_moves(piece[0:1], piece[1:], value_map, chess_board)
    output_moves(legal_moves, piece)

def map_initial_values(white, black, value_map, chess_board):
    for i, color in enumerate([black, white]):
        char = { 0: 'B', 1: 'W'}[i]

        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            indices = [value_map[j] for j in position]
            k, l = indices
            chess_board[l][k] = (piece_type, char) 

def generate_value_map():
    value_map = {}

    for i in range(8):
        value_map[chr(97+i)] = i
        value_map[str(i+1)] = i

    return value_map

def output_moves(legal_moves, piece):
    numbers = {}
    letters = {}

    for i in range(8):
        letters[i] = chr(97+i)
        numbers[i] = str(i+1)

    result = " ".join(sorted([letters[move[0]] + numbers[move[1]] for move in legal_moves]))

    print "LEGAL MOVES FOR " + piece + ": " + result

def validate_move(color, piece, pattern, chess_board, potential_move, potential_moves):
    k, l = potential_move
    p0, p1 = pattern
    inbounds = 0 <= k <= 7 and 0 <= l <= 7 
    occupying_color = inbounds and chess_board[l][k] and chess_board[l][k][1]
    valid_move = inbounds and color != occupying_color

    if valid_move:
        potential_moves.append(potential_move)

    if piece in ['Q', 'B', 'R'] and inbounds and not occupying_color:
        return validate_move(color, piece, pattern, chess_board, [k+p0, l+p1], potential_moves)
    else:
        return potential_moves

def get_move_patterns(piece_type):
    diagonal_movement = [[1, 1], [1, -1], [-1, +1], [-1, -1]]
    xy_movement = [[-1, 0], [1, 0], [0, 1], [0, -1]] 
    move_patterns = {
        "K": [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]],
        "N": [[-2, 1], [-1, 2], [1, 2], [2, 1], [-2, -1], [-1, -2], [2, -1], [1, -2]],
        "P": [[0, 1]],
        "B": diagonal_movement,
        "R": xy_movement,
        "Q": diagonal_movement + xy_movement
    }[piece_type]

    return move_patterns

def get_moves(piece_type, position, value_map, chess_board):
    indices = [value_map[i] for i in position]
    move_patterns = get_move_patterns(piece_type)
    potential_moves = []
    i, j = indices
    piece, color = chess_board[j][i]

    for pattern in move_patterns:
        p0, p1 = pattern
        potential_move = [i+p0, j+p1]
        legal_moves = validate_move(color, piece, pattern, chess_board, potential_move, potential_moves)

    return legal_moves

if __name__ == "__main__":
    main()
