"""
This module does so and so
"""

def main():
    """
    Main function todo docstring
    """

    #white = ['Rf1', 'Kg1', 'Bf2', 'Ph2', 'Pg3', 'Bf5']
    #black = ['Kb8', 'Qe8', 'Pa7', 'Pb7', 'Pc7', 'Qa6']
    white = ["Kg1", "Pg3"]
    black = ["Bf4", "Qc6", "Ph4"]

    chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]
    value_map = generate_value_map()
    piece = 'Qc6'
    map_initial_values(white, black, value_map['chr_to_ind'], chess_board)
    legal_moves = get_moves(piece[1:], value_map['chr_to_ind'], chess_board)
    output_moves(legal_moves, piece, value_map)

def map_initial_values(white, black, values, chess_board):
    """
    map_initial_values docstring Todo
    """

    for ind, color in enumerate([black, white]):
        char = {0: 'B', 1: 'W'}[ind]
        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            col, row = [values[j] for j in position]
            chess_board[row][col] = (piece_type, char)

def generate_value_map():
    """
    generate_value_map todo
    """

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
    """
    output_moves todo
    """

    numbers = value_map['ind_to_num']
    letters = value_map['ind_to_letter']
    values = " ".join(sorted([letters[move[0]] + numbers[move[1]] for move in legal_moves]))
    message = "LEGAL MOVES FOR {0}: {1}".format(piece, values)
    print message

def get_move_patterns(piece_type, color):
    """
    get_move_patterns todo
    """

    diagonal_movement = [[1, 1], [1, -1], [-1, +1], [-1, -1]]
    xy_movement = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    knight_movement = [[-2, 1], [-1, 2], [1, 2], [2, 1], [-2, -1], [-1, -2], [2, -1], [1, -2]]

    pawn_movement = {
        "W": [[0, 1], [-1, 1], [1, 1]],
        "B": [[0, -1], [-1, -1], [1, -1]]
    }[color]

    move_patterns = {
        "P": pawn_movement,
        "N": knight_movement,
        "B": diagonal_movement,
        "R": xy_movement,
        "K": diagonal_movement + xy_movement,
        "Q": diagonal_movement + xy_movement,
    }[piece_type]

    return move_patterns

def is_inbounds(indices):
    """
    is_indbound todo
    """

    row, column = indices
    return 0 <= row <= 7 and 0 <= column <= 7

def fetch_chess_piece(indices, chess_board):
    """
    fetch_chess_piece todo
    """

    col, row = indices
    return chess_board[row][col]

def recurse_check(original_move, check_move, pat, chess_board, check_pieces):
    """
    recurse_check todo
    """

    color = fetch_chess_piece(original_move, chess_board)[1]
    in_check = False

    if is_inbounds(check_move):
        new_piece_square = fetch_chess_piece(check_move, chess_board)
        if all(new_piece_square):
            new_piece, new_color = new_piece_square
            in_check = new_color != color and new_piece in check_pieces
        else:
            if 'Q' in check_pieces:
                new_check_move = add_pattern_to_move(check_move, pat)
                return recurse_check(original_move, new_check_move, pat, chess_board, check_pieces)

    return in_check


def validate_check(original_move, potential_move, chess_board):
    """
    validate_check todo
    """

    piece, color = fetch_chess_piece(original_move, chess_board)
    in_check = False

    for piece in ['P', 'B', 'R', 'N']:
        check_moves = get_move_patterns(piece, color)

        if piece == 'P':
            check_moves = check_moves[1:]

        check_pieces = [piece, 'Q'] if piece in ['B', 'R'] else [piece]

        for pat in check_moves:
            check_move = add_pattern_to_move(potential_move, pat)

            if original_move != check_move:
                in_check = recurse_check(original_move, check_move, pat, chess_board, check_pieces)

            if in_check:
                return in_check

    return False

def validate_move(pattern, chess_board, potential_move, moves, original_move):
    """
    validate_move todo
    """

    piece, color = fetch_chess_piece(original_move, chess_board)
    inbounds = is_inbounds(potential_move)

    occupying_color = inbounds and fetch_chess_piece(potential_move, chess_board)[1]

    #TODO: REFACTOR
    if piece == 'P':
        if pattern in [[0,1], [0,-1]]:
            valid_move = inbounds and not occupying_color
        else:
            valid_move = inbounds and occupying_color and color != occupying_color
    else:
        valid_move = inbounds and color != occupying_color

    if valid_move and piece == 'K':
        in_check = validate_check(original_move, potential_move, chess_board)
        valid_move = not in_check

    if valid_move:
        moves.append(potential_move)

    if piece in ['Q', 'B', 'R'] and inbounds and not occupying_color:
        new_move = add_pattern_to_move(potential_move, pattern)
        return validate_move(pattern, chess_board, new_move, moves, original_move)

    return moves

def add_pattern_to_move(indices, pattern):
    """
    add_pattern_to_move todo
    """

    row, col = indices
    row_pat, col_pat = pattern

    return [row + row_pat, col + col_pat]

def get_moves(position, values, chess_board):
    """
    get_moves todo
    """

    original_move = [values[i] for i in position]
    piece, color = fetch_chess_piece(original_move, chess_board)
    move_patterns = get_move_patterns(piece, color)
    moves = []

    for pattern in move_patterns:
        potential_move = add_pattern_to_move(original_move, pattern)
        legal_moves = validate_move(pattern, chess_board, potential_move, moves, original_move)

    return legal_moves

if __name__ == "__main__":
    main()
