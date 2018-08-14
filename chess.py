"""
This module does so and so
"""

def main():
    """Primary execution function.

    Gets valid input from user.
    Constructs chess board.
    Maps user input configuration to chess board.
    Outputs legal moves for a given piece
    """

    #creates a 8x8 array of tuples. The tuples will represent a piece's type and color.
    chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]

    white = validate_input("WHITE: ")
    black = validate_input("BLACK: ")
    piece = validate_input("PIECE TO MOVE: ")[0]

    #A dict of dicts that that maps indices to characters and vice versa
    value_map = generate_value_map()
    values = value_map['chr_to_ind']
    map_initial_values(white, black, values, chess_board)

    original_move = [values[i] for i in piece[1:]]
    legal_moves = get_moves(original_move, chess_board)
    output_moves(legal_moves, piece, value_map)

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

def generate_value_map():
    """Generates a value map from characters to indices and vice versa

    Returns:
        A dict of dicts of value mappings
    """

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

def map_initial_values(white, black, values, chess_board):
    """Places pieces onto the chessboard based on the user's board configuration.

    Args:
        white: An array of white pieces
        black: An array of black pieces
        values: A dict that maps characters to indices
        chess_board: An 8x8 multidemensional array of tuples
    """

    for ind, color in enumerate([black, white]):
        char = {0: 'B', 1: 'W'}[ind]

        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            col, row = [values[j] for j in position]
            chess_board[row][col] = (piece_type, char)

def get_moves(original_move, chess_board):
    """Gets all the legal moves for a piece

    Args:
        original_move: An array of indices that correspond to the original location of the piece
        chess_board: An 8x8 multidemensional array of tuples

    Returns:
        A list of lists containing indices that represent a piece's legal moves
    """

    piece, color = fetch_chess_piece(original_move, chess_board)
    move_patterns = get_move_patterns(piece, color)
    moves = []

    for pattern in move_patterns:
        potential_move = add_pattern_to_move(original_move, pattern)
        legal_moves = validate_move(pattern, chess_board, potential_move, moves, original_move)

    return legal_moves

def output_moves(legal_moves, piece, value_map):
    """Prints legal moves for a given piece

    Args:
        legal_moves: an array of legal moves
        piece: a string, the selected piece
        value_map: A dict of dicts of value mappings
    """

    numbers = value_map['ind_to_num']
    letters = value_map['ind_to_letter']
    values = " ".join(sorted([letters[move[0]] + numbers[move[1]] for move in legal_moves]))
    message = "LEGAL MOVES FOR {0}: {1}".format(piece, values)
    print message

def get_move_patterns(piece_type, color):
    """Accesses the movement patterns for a given piece

    Args:
        piece_type: A char representing a piece's type
        color: A char representing the color of the piece, used for pawn

    Returns:
        A list of movement patterns for the given piece
    """

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

def validate_move(pattern, chess_board, potential_move, moves, original_move):
    """Recursive function that finds all legal moves according to a movement pattern

    Args:
        pattern: An list consisting of how many squares to move vertically and horizontally
        chess_board: An 8x8 multidemensional array of tuples
        potential_move: An array of indices that correspond to a desired move
        moves: An array of all legal moves
        original_move: An array of indices that correspond to the original location of the piece

    Returns:
       An array of all legal moves.
    """

    piece, color = fetch_chess_piece(original_move, chess_board)
    inbounds = is_inbounds(potential_move)

    if not inbounds:
        return moves

    occupying_color = fetch_chess_piece(potential_move, chess_board)[1]
    valid_condition = color != occupying_color

    #pawn can only capture diagonally
    if piece == 'P':
        if pattern in [[0, 1], [0, -1]]: #vertical movement:
            valid_condition = not occupying_color
        else:
            valid_condition = occupying_color and color != occupying_color

    valid_move = valid_condition

    if valid_move and piece == 'K':
        valid_move = not determine_check(original_move, potential_move, chess_board)

    if valid_move:
        moves.append(potential_move)

    #For indeterminate pieces, recursively find all moves until another piece is encountered
    if piece in ['Q', 'B', 'R'] and not occupying_color:
        new_move = add_pattern_to_move(potential_move, pattern)
        return validate_move(pattern, chess_board, new_move, moves, original_move)

    return moves

def determine_check(original_move, potential_move, chess_board):
    """Determines if a King would be put in check for a potential move

    Args:
        original_move: An array of indices that correspond to the original location of the piece
        potential_move: An array of indices that correspond to a desired move
        chess_board: An 8x8 multidemensional array of tuples

    Returns:
       A bool, whether the King would be in check
    """

    piece, color = fetch_chess_piece(original_move, chess_board)
    in_check = False

    for piece in ['P', 'B', 'R', 'N']:
        check_moves = get_move_patterns(piece, color)

        if piece == 'P':
            check_moves = check_moves[1:] #pawn movement and capture patterns differ

        #Q shares movement patterns with B and R
        check_pieces = [piece, 'Q'] if piece in ['B', 'R'] else [piece]

        for pattern in check_moves:
            check_move = add_pattern_to_move(potential_move, pattern)

            if original_move != check_move: # don't evaluate the King's starting position
                in_check = recurse_check(color, check_move, pattern, chess_board, check_pieces)

            #exit if check is found
            if in_check:
                return in_check

    return False

def recurse_check(color, check_move, pattern, chess_board, check_pieces):
    """Recursive helper function for determine_check, evaluates squares for check

    Args:
        color: A string, the color of the King
        check_move: A list of indices representing a subsequent square on the board
        pattern: A list consisting of how many squares to move vertically and horizontally
        chess_board: An 8x8 multidemensional array of tuples
        check_pieces: A list of pieces that would yield check if encountered

    Returns:
        A bool, whether the King would be in check
    """

    in_check = False

    if is_inbounds(check_move):
        new_piece_square = fetch_chess_piece(check_move, chess_board)
        if all(new_piece_square): #Empty squares i.e. (0, 0) are truthy, hence the use of all
            new_piece, new_color = new_piece_square
            in_check = new_color != color and new_piece in check_pieces
        else:
            #For indeterminate pieces, check next square according to pattern
            if 'Q' in check_pieces:
                new_check_move = add_pattern_to_move(check_move, pattern)
                return recurse_check(color, new_check_move, pattern, chess_board, check_pieces)

    return in_check

def is_inbounds(indices):
    """A helper function to determine if a move would be inbounds

    Args:
        indices: an array of indices of a move

    Returns:
        A bool indicating if a move would be in bounds
    """

    row, column = indices
    return 0 <= row <= 7 and 0 <= column <= 7

def fetch_chess_piece(indices, chess_board):
    """A helper function to access pieces on the chess_board

    Args:
        indices: an array of indices
        chess_board: An 8x8 multidemensional array of tuples

    Returns:
        The the tuple found at the corresponding indices
    """

    col, row = indices
    return chess_board[row][col]

def add_pattern_to_move(indices, pattern):
    """Helper function to get indices of a new move after applying a movement pattern

    Args:
       indices: A list of indices for move
       pattern: A list consisting of how many squares to move vertically and horizontally

    Returns:
        An list of indices representing a new move on the chess board
    """

    row, col = indices
    row_pat, col_pat = pattern

    return [row + row_pat, col + col_pat]

if __name__ == "__main__":
    main()
