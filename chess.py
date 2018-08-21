"""
This module does so and so
"""

def main():
    """Primary execution function.

    Prompts for input.
    Builds chessboard.
    Creates a value map.
    Maps initial values to chessboard.
    Computes legal moves for a selected piece.
    Outputs legal moves.
    """
    cache = []

    white = validate_input("WHITE: ", cache)
    black = validate_input("BLACK: ", cache)
    piece = validate_input("PIECE TO MOVE: ", cache, evaluate_piece=True)[0]

    #creates a 8x8 array of tuples. The tuples will represent a piece's type and color.
    board = [[(0, 0) for _i in range(8)] for _j in range(8)]

    #A dict of dicts that that maps indices to characters and vice versa
    value_map = generate_value_map()

    char_map = value_map['chr_to_ind']
    map_initial_values(white, black, char_map, board)

    origin = [char_map[i] for i in piece[1:]]
    legal_moves = get_moves(origin, board)
    output_moves(legal_moves, piece, value_map)

def validate_input(prompt, cache, evaluate_piece=False):
    """Prompts for user input until valid, returns list of chess positions e.g ['Kg1', 'Bg2']

    When evaluate_piece is True, the list will be of a single value.
    """
    continue_input = True
    while continue_input:
        input_str = raw_input(prompt)
        values = sanitize_input(input_str)
        continue_input = has_invalid_values(values, evaluate_piece, cache)
    return values

def sanitize_input(input_str):
    """Sanitizes input and returns list of values from string"""
    #replace any commas with space, split will strip whitespace, only first chr upper
    return [val.capitalize() for val in input_str.replace(',', ' ').split()]

def has_invalid_values(values, evaluate_piece, cache):
    """Validates values list, return will continue/end while loop in validate_input"""
    try:
        validate_length(values, evaluate_piece)
        validate_position(values, evaluate_piece, cache)
    except ValueError as err:
        print err
        return True
    else:
        if not evaluate_piece:
            #Keep track of positions across different inputs to prevent repeating
            cache += [value[1:] for value in values]
        return False

def validate_length(values, evaluate_piece):
    """Raises ValueError if length of values is invalid"""
    if len(values) < 1:
        raise ValueError("\nInput cannot be blank\n")

    if evaluate_piece and len(values) > 1:
        raise ValueError("\nCannot evaluate moves for more than one piece\n")

def validate_position(values, evaluate_piece, cache):
    """Raises ValueError if a value's contents are invalid"""
    positions = []
    for value in values:
        position = value[1:]

        if len(value) != 3 or not validate_value(value):
            raise ValueError("\n{0} is not a valid input.\n".format(value))

        if evaluate_piece:
            if position not in cache:
                raise ValueError("\n{0} is not on the board".format(value))
        else:
            if position in cache or position in positions:
                raise ValueError("\n{0} is occupied\n".format(position))
            #keep track of positions within same input to prevent repetitions
            positions.append(position)

def validate_value(value):
    """Checks that a value only contins successive valid characters"""
    valid_chars = [
        ['K', 'Q', 'R', 'B', 'N', 'P'],
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
        ['1', '2', '3', '4', '5', '6', '7', '8'],
    ]

    for i, char in enumerate(list(value)):
        if not char in valid_chars[i]:
            return False

    return True

def generate_value_map():
    """Generates a value map from characters to indices and vice versa"""
    #Seperate dicts are needed for mapping indices back to characters otherwise keys would repeat
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

def map_initial_values(white, black, values, board):
    """Places pieces onto the chessboard based on the user's board configuration."""
    for i, color in enumerate([black, white]):
        char = {0: 'B', 1: 'W'}[i] #use index to access color char

        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            col, row = [values[j] for j in position]
            board[row][col] = (piece_type, char)

def get_moves(origin, board):
    """Returns all the legal moves for a piece"""
    piece, color = fetch_chess_piece(origin, board)
    move_patterns = get_move_patterns(piece, color)
    moves = []

    for pattern in move_patterns:
        potential_move = add_pattern_to_move(origin, pattern)
        legal_moves = validate_move(pattern, board, potential_move, moves, origin)

    return legal_moves

def get_move_patterns(piece_type, color):
    """Accesses the movement patterns for a given piece"""
    diagonal_movement = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    xy_movement = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    knight_movement = [[-2, 1], [-1, 2], [1, 2], [2, 1], [-2, -1], [-1, -2], [2, -1], [1, -2]]

    #chessboard orientation is absolute, so white pawns move up, and black pawns move down
    pawn_movement = {
        "W": [[0, 1], [-1, 1], [1, 1]],
        "B": [[0, -1], [-1, -1], [1, -1]]
    }[color] #use color to access relevant pawn patterns

    move_patterns = {
        "P": pawn_movement,
        "N": knight_movement,
        "B": diagonal_movement,
        "R": xy_movement,
        "K": diagonal_movement + xy_movement,
        "Q": diagonal_movement + xy_movement,
    }[piece_type] #use piece_type to access relevant patterns

    return move_patterns

def validate_move(pattern, board, potential_move, moves, origin):
    """Recursive function that finds all legal moves according to a movement pattern"""
    piece, color = fetch_chess_piece(origin, board)

    if not is_inbounds(potential_move):
        return moves

    potential_color = fetch_chess_piece(potential_move, board)[1]
    empty = not potential_color
    capturable = potential_color and color != potential_color
    valid_move = empty or capturable

    #pawn can only move to vertically and capture diagonally
    if piece == 'P':
        valid_move = empty if pattern in [[0, 1], [0, -1]] else capturable

    if piece == 'K' and valid_move:
        valid_move = not determine_check(origin, potential_move, board)

    if valid_move:
        moves.append(potential_move)

    #For indeterminate pieces, recursively find all moves until another piece is encountered
    if piece in ['Q', 'B', 'R'] and not potential_color:
        new_move = add_pattern_to_move(potential_move, pattern)
        return validate_move(pattern, board, new_move, moves, origin)

    return moves

def determine_check(origin, potential_move, board):
    """Determines if a King would be put in check for a potential move"""
    piece, color = fetch_chess_piece(origin, board)
    in_check = False

    for piece in ['P', 'B', 'R', 'N']:
        check_moves = get_move_patterns(piece, color)

        if piece == 'P':
            check_moves = check_moves[1:] #pawn movement and capture patterns differ

        #Q shares movement patterns with B and R
        check_pieces = [piece, 'Q'] if piece in ['B', 'R'] else [piece]

        for pattern in check_moves:
            check_move = add_pattern_to_move(potential_move, pattern)

            if origin != check_move: # don't evaluate the King's starting position
                in_check = recurse_check(color, check_move, pattern, board, check_pieces)

            #exit if check is found
            if in_check:
                return True

    return False

def recurse_check(color, check_move, pattern, board, check_pieces):
    """Recursive helper function for determine_check, evaluates squares for check"""
    in_check = False

    if is_inbounds(check_move):
        new_piece_square = fetch_chess_piece(check_move, board)
        if all(new_piece_square): #Empty squares i.e. (0, 0) are truthy, hence the use of all
            new_piece, new_color = new_piece_square
            in_check = new_color != color and new_piece in check_pieces
        else:
            #For indeterminate pieces, check next square according to pattern
            if 'Q' in check_pieces:
                new_check_move = add_pattern_to_move(check_move, pattern)
                return recurse_check(color, new_check_move, pattern, board, check_pieces)

    return in_check

def is_inbounds(indices):
    """A helper function to determine if a move would be inbounds"""
    col, row = indices
    return 0 <= row <= 7 and 0 <= col <= 7

def fetch_chess_piece(indices, board):
    """A helper function to access pieces on the board """
    col, row = indices
    return board[row][col]

def add_pattern_to_move(indices, pattern):
    """Helper function to get indices of a new move after applying a movement pattern"""
    col, row = indices
    col_pat, row_pat = pattern
    return [col + col_pat, row + row_pat]

def output_moves(legal_moves, piece, value_map):
    """Prints legal moves for a given piece"""
    numbers = value_map['ind_to_num']
    letters = value_map['ind_to_letter']
    values = " ".join(sorted([letters[move[0]] + numbers[move[1]] for move in legal_moves]))
    message = "LEGAL MOVES FOR {0}: {1}".format(piece, values)
    print message

if __name__ == "__main__":
    main()
