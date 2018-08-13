"""
This module does so and so
"""

def validate_input(prompt):
    """Validates a input from the user and splits the string input to an array of chess positions

    Args:
       prompt (string): A message to display to the user to prompt for input

    Returns:
        An array of chess pieces with their positions, ex. ['Kg1', 'Rf2']
    """

    not_valid = True

    valid_pieces = ['K', 'Q', 'R', 'B', 'N', 'P']
    valid_rows = ['1', '2', '3', '4', '5', '6', '7', '8']
    valid_cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    while not_valid:
        input_string = raw_input(prompt)

        #sanitize input -- piece type upper, position lower.
        values = [value[0:1].upper() + value[1:].lower() for value in input_string.split()]

        try:
            for value in values:

                #isolate relevant portions of the string and check they are valid
                valid_piece = value[0:1] in valid_pieces
                valid_col = value[1:2] in valid_cols
                valid_row = value[2:] in valid_rows

                if not valid_piece or not valid_row or not valid_col:
                    err_msg = "\n{0} is not a valid input. Please try again.\n".format(value)
                    raise ValueError(err_msg)

            not_valid = False #if no errors are encountered, end outer while loop

        except ValueError as err:
            print err

    return values

def main():
    """Primary execution function."""

    #creates a 8x8 array of tuples. The tuples will represent a piece's type and color.
    chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]

    #A dict of dicts that that maps indices to characters and vice versa
    value_map = generate_value_map()

    white = validate_input("WHITE: ")
    black = validate_input("BLACK: ")
    piece = validate_input("PIECE TO MOVE: ")[0]


    #white = ['Rf1', 'Kg1', 'Bf2', 'Ph2', 'Pg3', 'Bf5']
    #black = ['Kb8', 'Qe8', 'Pa7', 'Pb7', 'Pc7', 'Qa6']

    #white = ["Kg1", "Pg3"]
    #black = ["Bf4", "Qc6", "Ph4"]

    #piece = "Kg1"

    map_initial_values(white, black, value_map['chr_to_ind'], chess_board)
    legal_moves = get_moves(piece[1:], value_map['chr_to_ind'], chess_board)
    output_moves(legal_moves, piece, value_map)

def map_initial_values(white, black, values, chess_board):
    """
    Places pieces onto the chessboard based on the user's board configuration.

    Args:
        white: An array of white pieces
        black: An array of black pieces
        values: A dict that maps characters to indices
        chess_board: An 8x8 multidemensional array of tuples

    Ex:
        If black has the piece Rf1, the value at chess_board[0][5] will equal ('R', 'B')

        A chess piece's horizontal and vertical position is mapped to array indices
        Using this mapping, a piece's type and color are stored in a tuple at those indices
        On the chessboard, letters correspond to columns while the numbers correspond to rows
        In a multidimensional array we need the row first (number) and the column second (letter).
    """

    for ind, color in enumerate([black, white]):
        char = {0: 'B', 1: 'W'}[ind]

        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            col, row = [values[j] for j in position]
            chess_board[row][col] = (piece_type, char)

def generate_value_map():
    """Generates a value map from characters to indices and vice versa

    Returns:
        A dict of dicts of value mappings

    Ex:
        chr_to_ind = { 'a': 0, 'b': 1, '1': 0, '2': 1 ... }
        ind_to_num = { 0: '1', 1: '2' ... }
        ind_to_letter = { 0: 'a', 1: 'b' ...}

        Seperate dicts are needed for mapping indices back to characters otherwise keys would repeat

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

    if not inbounds:
        return moves

    occupying_color = fetch_chess_piece(potential_move, chess_board)[1]
    valid_condition = color != occupying_color

    if piece == 'P':
        if pattern in [[0, 1], [0, -1]]:
            valid_condition = not occupying_color
        else:
            valid_condition = occupying_color and color != occupying_color

    valid_move = valid_condition

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
