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

    VALID_CHARS = [
        ['K', 'Q', 'R', 'B', 'N', 'P'],
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
        ['1', '2', '3', '4', '5', '6', '7', '8'],
    ]

    cache = []

    white = validate_input("WHITE: ", VALID_CHARS, cache)
    black = validate_input("BLACK: ", VALID_CHARS, cache)
    piece = validate_input("PIECE TO MOVE: ", VALID_CHARS, cache, evaluate_piece=True)[0]

    #creates a 8x8 array of tuples. The tuples will represent a piece's type and color.
    chess_board = [[(0, 0) for _i in range(8)] for _j in range(8)]

    #A dict of dicts that that maps indices to characters and vice versa
    value_map = generate_value_map()

    char_map = value_map['chr_to_ind']
    map_initial_values(white, black, char_map, chess_board)

    origin = [char_map[i] for i in piece[1:]]
    legal_moves = get_moves(origin, chess_board)
    output_moves(legal_moves, piece, value_map)

def validate_input(prompt, VALID_CHARS, cache, evaluate_piece=False):
    """Validates a input from the user and splits the string input to an array of chess positions

    Args:
       prompt (string): A message to display to the user to prompt for input

    Returns:
        A list of chess pieces with their positions, ex. ['Kg1', 'Rf2']
    """

    while True:
        input_string = raw_input(prompt)
        played_positions = []

        #sanitize input -- piece type upper, position lower.
        values = [value[0:1].upper() + value[1:].lower() for value.split() in input_string.split()]

        try:
            if len(values) < 1:
                raise ValueError("\nInput cannot be blank\n")

            if evaluate_piece and len(values) > 1:
                raise ValueError("\nCannot evaluate moves for more than one piece\n")

            for value in values:
                position = value[1:]

                if len(value) != 3 or not validate_value(value, VALID_CHARS):
                    raise ValueError("\n{0} is not a valid input.\n".format(value))

                if evaluate_piece:
                    if position not in cache:
                        raise ValueError("\n{0} is not on the board".format(value))
                else:
                    if position in cache or position in played_positions:
                        raise ValueError("\n{0} is occupied\n".format(position))
                    played_positions.append(position)

        except ValueError as err:
            print err
        else:
            if not evaluate_piece:
                cache += played_positions
            break #end while loop

    return values

def validate_value(value, VALID_CHARS):
    for i, char in enumerate(list(value)):
        if not char in VALID_CHARS[i]:
            return False

    return True

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
        white: A list of white pieces
        black: A list of black pieces
        values: A dict that maps characters to indices
        chess_board: An 8x8 2d list of tuples
    """

    for ind, color in enumerate([black, white]):
        char = {0: 'B', 1: 'W'}[ind]

        for played_piece in color:
            piece_type = played_piece[0:1]
            position = played_piece[1:]
            col, row = [values[j] for j in position]
            chess_board[row][col] = (piece_type, char)

def get_moves(origin, chess_board):
    """Gets all the legal moves for a piece

    Args:
        origin: A list of indices that correspond to the original location of the piece
        chess_board: An 8x8 2d list of tuples

    Returns:
        A list of lists containing indices that represent a piece's legal moves
    """

    piece, color = fetch_chess_piece(origin, chess_board)
    move_patterns = get_move_patterns(piece, color)
    moves = []

    for pattern in move_patterns:
        potential_move = add_pattern_to_move(origin, pattern)
        legal_moves = validate_move(pattern, chess_board, potential_move, moves, origin)

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

def validate_move(pattern, chess_board, potential_move, moves, origin):
    """Recursive function that finds all legal moves according to a movement pattern

    Args:
        pattern: An list consisting of how many squares to move vertically and horizontally
        chess_board: An 8x8 2d list of tuples
        potential_move: A list of indices that correspond to a desired move
        moves: A list of all legal moves
        origin: A list of indices that correspond to the original location of the piece

    Returns:
       A list of all legal moves.
    """

    piece, color = fetch_chess_piece(origin, chess_board)
    inbounds = is_inbounds(potential_move)

    if not inbounds:
        return moves

    potential_color = fetch_chess_piece(potential_move, chess_board)[1]
    valid_move = color != potential_color #either empty or capturable

    #pawn can only capture diagonally
    if piece == 'P':
        if pattern in [[0, 1], [0, -1]]: #vertical movement:
            valid_move = not potential_color
        else:
            valid_move = valid_move and potential_color #can only capture if opposing piece

    if piece == 'K' and valid_move:
        valid_move = not determine_check(origin, potential_move, chess_board)

    if valid_move:
        moves.append(potential_move)

    #For indeterminate pieces, recursively find all moves until another piece is encountered
    if piece in ['Q', 'B', 'R'] and not potential_color:
        new_move = add_pattern_to_move(potential_move, pattern)
        return validate_move(pattern, chess_board, new_move, moves, origin)

    return moves

def determine_check(origin, potential_move, chess_board):
    """Determines if a King would be put in check for a potential move

    Args:
        origin: A list of indices that correspond to the original location of the piece
        potential_move: A list of indices that correspond to a desired move
        chess_board: An 8x8 2d list of tuples

    Returns:
       A bool, whether the King would be in check
    """

    piece, color = fetch_chess_piece(origin, chess_board)
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
        chess_board: An 8x8 2d list of tuples
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
        chess_board: An 8x8 2d list of tuples

    Returns:
        The tuple found at the corresponding indices
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
