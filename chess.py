def main(black=[], white=[], piece=None):
    #white = ['Rf1', 'Kg1', 'Bf2', 'Ph2', 'Pg3', 'Bf5']
    #black = ['Kb8', 'Qe8', 'Pa7', 'Pb7', 'Pc7', 'Qa6']
    white = ["Kg1"]
    black = ["Qc6", "Bf4", "Pg2"]

    chess_board = [[0 for i in range(8)] for j in range(8)]
    value_map = generate_value_map()
    piece = 'Kg1'
    map_initial_values(white, black, value_map['chr_to_ind'], chess_board)
    legal_moves = get_moves(piece[0:1], piece[1:], value_map['chr_to_ind'], chess_board)
    output_moves(legal_moves, piece, value_map)

def map_initial_values(white, black, values, chess_board):
    for i, color in enumerate([black, white]):
        char = {0: 'B', 1: 'W'}[i]
        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            k, l = [values[j] for j in position]
            chess_board[l][k] = (piece_type, char)

def generate_value_map():
    value_map = {
        'chr_to_ind': {},
        'ind_to_num': {},
        'ind_to_letter': {}
    }

    for i in range(8):
        letter = chr(97+i)
        number = str(i+1)

        value_map['chr_to_ind'][letter] = i
        value_map['chr_to_ind'][number] = i
        value_map['ind_to_num'][i] = number
        value_map['ind_to_letter'][i] = letter

    return value_map

def output_moves(legal_moves, piece, value_map):
    numbers = value_map['ind_to_num']
    letters = value_map['ind_to_letter']
    values = " ".join(sorted([letters[move[0]] + numbers[move[1]] for move in legal_moves]))
    message = "LEGAL MOVES FOR {0}: {1}".format(piece, values)
    print message

def get_move_patterns(piece_type, color):
    diagonal_movement = [[1, 1], [1, -1], [-1, +1], [-1, -1]]
    xy_movement = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    knight_movement = [[-2, 1], [-1, 2], [1, 2], [2, 1], [-2, -1], [-1, -2], [2, -1], [1, -2]]
    pawn_movement = [[0, 1]] if color is 'W' else [[0, -1]]
    move_patterns = {
        "P": pawn_movement,
        "N": knight_movement,
        "B": diagonal_movement,
        "R": xy_movement,
        "K": diagonal_movement + xy_movement,
        "Q": diagonal_movement + xy_movement,
    }[piece_type]

    return move_patterns

def get_capture_patterns(piece, color):
    capture_patterns = []

    if piece == "P":
       capture_patterns = {
           "W": [[-1, 1], [1, 1]],
           "B": [[-1, -1], [1, -1]]
       }[color]
    else:
        capture_patterns = get_move_patterns(piece, color)

    return capture_patterns

def is_inbounds(i, j):
    return 0 <= i <= 7 and 0 <= j <= 7

def recurse_check(original_move, check_move, pat, chess_board, check_pieces):
    i, j = original_move
    piece, color = chess_board[j][i]
    in_check = False
    y, z = check_move

    if is_inbounds(y, z):
        if chess_board[z][y]:
            new_piece, new_color = chess_board[z][y]
            in_check = new_color != color and new_piece in check_pieces
        else:
            if 'Q' in check_pieces:
                return recurse_check(original_move, [y+pat[0], z+pat[1]], pat, chess_board, check_pieces)

    return in_check


def validate_check(original_move, potential_move, chess_board):
    i, j = original_move
    k, l = potential_move
    piece, color = chess_board[j][i]
    in_check = False

    for piece in ['P', 'B', 'R', 'N']:
        check_moves = get_capture_patterns(piece, color)
        check_pieces = [piece, 'Q'] if piece in ['B', 'R'] else [piece]

        for x, pat in enumerate(check_moves):
            check_move = [k+pat[0], l+pat[1]]

            if original_move != check_move:
                in_check = recurse_check(original_move, check_move, pat, chess_board, check_pieces)

            if in_check:
                return in_check

    return False

def validate_move(pattern, chess_board, potential_move, moves, original_move):
    i, j = original_move
    piece, color = chess_board[j][i]
    k, l = potential_move
    inbounds = is_inbounds(k, l)

    occupying_color = inbounds and chess_board[l][k] and chess_board[l][k][1]
    valid_move = inbounds and color != occupying_color

    if valid_move and piece == 'K':
        in_check = validate_check(original_move, potential_move, chess_board)
        valid_move = not in_check

    if valid_move:
        moves.append(potential_move)

    if piece in ['Q', 'B', 'R'] and inbounds and not occupying_color:
        p0, p1 = pattern
        return validate_move(pattern, chess_board, [k+p0, l+p1], moves, original_move)
    else:
        return moves

def get_moves(piece_type, position, values, chess_board):
    original_move = [values[i] for i in position]
    i, j = original_move
    piece, color = chess_board[j][i]
    move_patterns = get_move_patterns(piece, color)
    moves = []
    

    for pattern in move_patterns:
        p0, p1 = pattern
        potential_move = [i+p0, j+p1]
        legal_moves = validate_move(pattern, chess_board, potential_move, moves, original_move)

    return legal_moves

if __name__ == "__main__":
    main()
