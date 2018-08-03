def main(black=[], white=[], piece=None):
    #white = ['Rf1', 'Kg1', 'Bf2', 'Ph2', 'Pg3', 'Bf5']
    #black = ['Kb8', 'Qe8', 'Pa7', 'Pb7', 'Pc7', 'Qa6']
    white = ["Kg1"]
    black = ["Qc6",  "Bf4", "Re2" ]

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
            indices = [values[j] for j in position]
            k, l = indices
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

def get_move_patterns(piece_type):
    diagonal_movement = [[1, 1], [1, -1], [-1, +1], [-1, -1]]
    xy_movement = [[-1, 0], [1, 0], [0, 1], [0, -1]] 
    knight_movement = [[-2, 1], [-1, 2], [1, 2], [2, 1], [-2, -1], [-1, -2], [2, -1], [1, -2]]
    move_patterns = {
        "P": [[0, 1]],
        "N": knight_movement,
        "B": diagonal_movement,
        "R": xy_movement,
        "K": diagonal_movement + xy_movement, 
        "Q": diagonal_movement + xy_movement,
    }[piece_type]

    return move_patterns

def validate_check(original_move, potential_move, chess_board, color, check_moves, check_pieces):
    k, l = potential_move

    for x, pat in enumerate(check_moves):

        check_move = [k+pat[0], l+pat[1]]
        y, z = check_move

        next_move = True
        while next_move and original_move != check_move:
            next_move = 0 <= z <= 7 and 0 <= y <= 7 

            if next_move:
                if not chess_board[z][y]:
                    z += pat[1]
                    y += pat[0]
                else:
                    new_piece, new_color = chess_board[z][y]

                    if new_color != color and new_piece in check_pieces:
                        return True

                    next_move = False

    return False

def validate_move(color, piece, pattern, chess_board, potential_move, moves, original_move):
    k, l = potential_move
    inbounds = 0 <= k <= 7 and 0 <= l <= 7 
    occupying_color = inbounds and chess_board[l][k] and chess_board[l][k][1]
    valid_move = inbounds and color != occupying_color


    if valid_move and piece == 'K':
        in_check = False 
        diagonal_moves = get_move_patterns('B')
        xy_moves = get_move_patterns('R')
        knight_moves = get_move_patterns('N')

#        for check_moves in [diagonal_moves, xy_moves, knight_moves]:
 #           in_check = validate_check(original_move, potential_move, chess_board, color, check_moves)

        in_check = validate_check(original_move, potential_move, chess_board, color, diagonal_moves, ['B', 'Q']) 
        knight_check = validate_check(original_move, potential_move, chess_board, color, knight_moves, ['N']) 
        xy_check = validate_check(original_move, potential_move, chess_board, color, xy_moves, ['R'])
        

        print "diagonal", in_check
        print "knight", knight_check
        print "xy", xy_check


        valid_move = not in_check

    if valid_move:
        moves.append(potential_move)

    if piece in ['Q', 'B', 'R'] and inbounds and not occupying_color:
        p0, p1 = pattern
        return validate_move(color, piece, pattern, chess_board, [k+p0, l+p1], moves, original_move)
    else:
        return moves

def get_moves(piece_type, position, values, chess_board):
    original_move = [values[i] for i in position]
    move_patterns = get_move_patterns(piece_type)
    moves = []
    i, j = original_move
    piece, color = chess_board[j][i]

    for pattern in move_patterns:
        p0, p1 = pattern
        potential_move = [i+p0, j+p1]
        legal_moves = validate_move(color, piece, pattern, chess_board, potential_move, moves, original_move)

    return legal_moves

if __name__ == "__main__":
    main()
