"""
connectfour.py

A Connect Four game in Python.
"""

import random

# Constants
# Board dimensions
BOARD_WIDTH = 7
BOARD_HEIGHT = 6

# Computer intelligence range (1 is the lowest)
MIN_INTELLIGENCE = 0
MAX_INTELLIGENCE = 4
HUMAN_PLAYER = -1

# Symbols to draw the board (0th entry is a blank, 1st entry is player 1, 2nd entry is player 2)
BOARD_SYMBOLS = [ ' ', 'X', 'O' ]

def make_board(width = BOARD_WIDTH, height = BOARD_HEIGHT):
    """
        Create a new Connect Four board, which is stored in a 1-dimensional integer array with width * height
        entries.  The entries of the board are stored in row-major order, starting at the first row.  Each entry
        in the array is one of the following integers:

            0   =   Blank space
            1   =   Player 1's piece occupies the space
            2   =   Player 2's piece occupies the space.
    """

    return [ 0 for i in range(0,height * width) ]


def board_xy_to_ind(row,col, width = BOARD_WIDTH, height = BOARD_HEIGHT):
    """ Convert (row,col) on board to index into the board array.  Coordinates start in upper-left hand
        corner of the board.

            row = row of the board (starting at 0)
            col = column of the board (starting at 0)

        Returns index into board array if (row,col) are valid, and -1 if (row,col) is invalid.
    """
    if row < 0 or row >= BOARD_HEIGHT or col < 0 or col >= BOARD_WIDTH:
        # Invalid coordinates.
        return -1

    return row * width + col

def max_num_player_symbols(start_row, start_col, row_stride, col_stride, player,board, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    """ Starting at (start_row,start_col), check for the maximum number of consecutive symbols in a certain path
        of board entries around (start_row,start_col).  In particular, look within a "radius" of three slots from
        (start_row,start_col).  row_stride and col_stride determine the orientation of the path around (start_row,
        start_col).  For example, row_stride = -1 and col_stride = 1 results in a path up to and the right,
        beginning at (start_row + 3, start_col - 3).

            start_row = starting row
            start_col = starting column
            row_stride = change to the row index at each iteration
            col-stride = change to the col index at each iteration
            player = player whose pieces should be checked (1 or 2)
            board = the board array

        Returns a non-negative integer equal to the maximum number of consecutive player symbols encountered on
        the indicated path.
    """
    max_syms = 0
    cur_count = 0

    # Start the location a vertical distance of -3 * row_stride and a horizontal distance -3 * rowstride from
    # the position (start_row,start_col).
    row = start_row - row_stride * 3
    col = start_col - col_stride * 3

    # Check the seven consecutive board spaces starting at the starting position and moving by col_stride columns and
    # row_stride rows at end iteration.  Keep track of the maximum number of symbols in a row you encounter.
    for i in range(0,8):
        ind = board_xy_to_ind(row,col,width,height)
        if ind != -1:
            # Valid board coordinate.
            if board[ind] == player:
                # Another consecutive piece from this player.
                cur_count = cur_count + 1
                if cur_count > max_syms:
                    # A new record!  Update the max_syms count.
                    max_syms = cur_count
            else:
                # This slot is not taken up by the player's piece.  Reset the current symbol count.
                cur_count = 0

        # Stride to the next board slot on the path.
        row = row + row_stride
        col = col + col_stride
    return max_syms

def has_player_won(row, col, player, board, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    """ Determine if the player's move at (row,col) was a winning move.  Coordinates start in upper-left
        hand corner of the board.

            row = row of the board (starting at 0)
            col = column of the board (starting at 0)
            player = player (1 or 2)
            board = the board

        Returns True if the move was a winning move, and False otherwise.
    """

    # Check horizontally (no row stride but a col stride of 1).
    if max_num_player_symbols(row,col,0,1,player,board) >= 4:
        return True

    # Check vertically (no col stride, but a row stride of 1)
    if max_num_player_symbols(row,col,1,0,player,board) >= 4:
        return True

    # Check diagonally down and to the right (row and col strides of 1)
    if max_num_player_symbols(row,col,1,1,player,board) >= 4:
        return True

    # Check diagonally up and to the right (row stride of -1 (to go up) and col stride of 1)
    return max_num_player_symbols(row,col,-1,1,player,board) >= 4

def tab_str(tab = 6):
    # Print a tab of tab blank characters.
    return ' ' * tab

def print_board(board, width = BOARD_WIDTH, height = BOARD_HEIGHT, display_player_syms = True):
    # Print the board.  display_player_syms == True means the player legend is displayed.
    # Print the labels.
    for i in range(1,3):
        print(f'Player {i} is {BOARD_SYMBOLS[i]}.  ',end='')
    print('\n')

    # Print the column numbers
    print(tab_str(),end='')
    for i in range(0,width):
        print('  ' + str(i+1) + ' ',end='')
    print('')

    # Print the top of the board
    print(tab_str() + '____'*BOARD_WIDTH + '_')

    # Print the rest of the board.
    for y in range(0,height):
        print(tab_str(),end='')
        for x in range(0,width):
            print('| ',end='')
            print(BOARD_SYMBOLS[board[y*width + x]] + ' ',end='')
        print('|')

    # Print the bottom of the board.
    print(tab_str() + '----' * BOARD_WIDTH + '-')

def is_column_full(column, board, width = BOARD_WIDTH):
    # Determines if the indicated column is full.
    return board[column] != 0

def is_board_full(board, width = BOARD_WIDTH):
    # Determines if the indicated column is full.
    for col in range(0,width):
        if not is_column_full(col,board,width):
            return False        #   Found an empty column

    # All the columns are full.
    return True

def drop_piece(column, num_filled_spaces_in_col, player, board, width = BOARD_WIDTH, height = BOARD_HEIGHT):
    # Return the row where the piece was dropped (-1 if there was no space in this column).
    if num_filled_spaces_in_col[column] >= BOARD_HEIGHT:
        # There is no empty space in this column.
        return -1

    # This column has space.  Put the piece here and return the row number.
    # i is the row into which the space will be dropped (with the 0th row being the top).
    i = height - num_filled_spaces_in_col[column] - 1
    board[i*width + column] = player
    num_filled_spaces_in_col[column] = num_filled_spaces_in_col[column] + 1
    return i

def drop_random_col(player, num_filled_spaces_in_col, board, width = BOARD_WIDTH, height = BOARD_HEIGHT):
    # Drop in a random column
    # First find the open columns
    empty_cols = [i for i,val in enumerate(num_filled_spaces_in_col) if val < BOARD_HEIGHT ]

    # Choice a random open column
    column = random.choice(empty_cols)
    row_dropped = height - num_filled_spaces_in_col[column] - 1
    return (row_dropped, column)

def find_winning_move(player,num_filled_spaces_in_col, board, width = BOARD_WIDTH, height = BOARD_HEIGHT):
    # Determine if player's next move can be a winning move.
    # Return -1 if there is no winning move available.
    empty_cols = [i for i, val in enumerate(num_filled_spaces_in_col) if val < BOARD_HEIGHT ]
    tmp_board = board.copy()

    for col in empty_cols:
        test_row = height - num_filled_spaces_in_col[col] - 1
        i = test_row * width + col
        tmp_board[i] = player
        if has_player_won(test_row,col,player,tmp_board,width,height):
            # Winning move
            return (test_row, col)
        tmp_board[i] = 0

    # No winning move available.
    return (-1,-1)

def block_winning_move(player,num_filled_spaces_in_col, board, width = BOARD_WIDTH, height = BOARD_HEIGHT):
    # Determine if the other player has a winning move, in which case player should block it.
    # Return -1 if there is no winning move by the other player to block.
    other_player = 1
    if player == 1:
        other_player = 2

    return find_winning_move(other_player,num_filled_spaces_in_col, board, width, height)

def drop_random_col_but_check_for_loss(player, num_filled_spaces_in_col, board, width = BOARD_WIDTH, height = BOARD_HEIGHT):
    # Drop in a random column that does not give the other player the opportunity to win in the next move.
    # Return (-1,-1) if dropping in any open column would give the other player the opportunity to win.
    empty_cols = [i for i,val in enumerate(num_filled_spaces_in_col) if val < BOARD_HEIGHT ]
    random.shuffle(empty_cols)
    tmp_board = board.copy()
    tmp_num_filled_spaces_in_col = num_filled_spaces_in_col.copy()
    other_player = 1
    if player == 1:
        other_player = 2

    for i in range(len(empty_cols)):
        column = empty_cols[i]
        row_dropped = height - tmp_num_filled_spaces_in_col[column] - 1
        tmp_board[row_dropped * width + column] = player
        tmp_num_filled_spaces_in_col[column] += 1
        if find_winning_move(other_player,tmp_num_filled_spaces_in_col, tmp_board, width, height) == (-1,-1):
            # It's safe to drop here.
            return (row_dropped, column)

        # Don't drop there; it will allow the other player to win in the next move.
        # Rest the temporary board
        tmp_board[row_dropped * width + column] = 0
        tmp_num_filled_spaces_in_col[column] -= 1

    # If you get to this point, there is no column you can randomly drop into that won't result in an opportunity
    # for the other player to win during his next move.
    return (-1,-1)

# Create intelligence process for computer.  The intelligence # is determined by a list of move functions to be
# executed in a particular order, with one list for each # intelligence level.  Dumbest intelligence starts at the
# beginning of the list.
# Each function in the list has the signature (player,num_filled_spaces_in_col,board,width_height) and returns
# a 2-tuple consisted of the row and column where the next move should be.  row = -1 in the 2-tuple if there is
# no available move under that step.
COMPUTER_MOVE_STEPS = [
    [],
    [find_winning_move],
    [block_winning_move, find_winning_move],
    [find_winning_move, block_winning_move],
    [find_winning_move, block_winning_move, drop_random_col_but_check_for_loss]
]
def computer_move(comp_intel, player, num_filled_spaces_in_col, board, width = BOARD_WIDTH, height = BOARD_HEIGHT):
    # Returns the tuple (row_dropped, column).
    row_dropped = -1
    column = 0

    # Interate through the process of possible moves (based on the computer's intelligence level).
    for move in COMPUTER_MOVE_STEPS[comp_intel]:
        row_dropped, column = move(player, num_filled_spaces_in_col, board, width, height)
        if row_dropped != -1:
            break

    if row_dropped == -1:
        # The process above was unable to determine any move.  Do a random move as a last resort.
        row_dropped, column = drop_random_col(player, num_filled_spaces_in_col, board, width, height)

    # Update the board and column counter
    board[row_dropped * width + column] = player
    num_filled_spaces_in_col[column] = num_filled_spaces_in_col[column] + 1

    return (row_dropped, column)

def get_human_move(round,num_filled_spaces_in_col,cur_player,board):
    # Get a human player's move.  Returns (row_dropped, column), which row_dropped = -1 if the player
    # gives invalid input.
    row_dropped = 0
    column = 0
    try:
        column_str = input(f'Round {round}: Player {cur_player}, please enter the number of the column where you want to drop your piece. ')
        print('')  # Always make sure there is a blank line before the next console output.
        column = int(column_str) - 1
    except:
        print('\t*** Invalid entry.  Please enter a valid column number. ***\n')
        return (-1,0)

    if column < 0 or column >= BOARD_WIDTH:
        print('\t*** Invalid entry.  Please enter a valid column number. ***\n')
        return (-1,0)
    else:
        row_dropped = drop_piece(column, num_filled_spaces_in_col, cur_player, board)
        if row_dropped == -1:
            # That column is full.
            print(f'\t*** Column {column + 1} is full.  Please select a different column. ***\n')
            return (-1,0)

    return (row_dropped,column)

def play_connect_four(comp_player_vec):
    # Main playing loop for a two-player game.
    # comp_player_vec determines which players are the computer.

    board = make_board()
    num_filled_spaces_in_col = [0] * BOARD_WIDTH    #   Number of filled spaces in each column.

    # Remember that player index here starts at one, whereas the comp_player_vec's index starts at zero!
    cur_player = 1
    round = 1
    column = 0
    who_won = -1
    row_dropped = 0
    column = 0

    print('Welcome to Connect Four!  Let\'s get started!\n')

    while(round <= BOARD_WIDTH * BOARD_HEIGHT / 2):
        print_board(board)
        print('')

        if comp_player_vec[cur_player - 1] == HUMAN_PLAYER:
            # Current player is human.
            row_dropped, column = get_human_move(round,num_filled_spaces_in_col,cur_player,board)
            if row_dropped == -1:
                # Invalid entry.  Asked again.
                continue
        else:
            # Current player is the computer.
            row_dropped, column = computer_move(comp_player_vec[cur_player - 1],cur_player,num_filled_spaces_in_col,board)
            print(f'\nRound {round}: Player {cur_player} dropped his piece in column {column + 1}.\n')

        # Successful drop!
        # Check if the current player won.
        if has_player_won(row_dropped, column, cur_player, board):
            # Current player won
            who_won = cur_player
            break

        # Now switch to the next player (and round if the current player is player two.
        if cur_player == 1:
            cur_player = 2
        else:
            cur_player = 1
            round = round + 1
            if comp_player_vec[0] != HUMAN_PLAYER and comp_player_vec[1] != HUMAN_PLAYER:
                # Pause for user input at the end of the round so that game doesn't fly by.
                print_board(board)
                print('')
                input('Press enter to continue to the next round. ')

    # The board is full.  Print the board one last time, then end the game.  It's a draw.
    print_board(board)

    if who_won == -1:
        # No one won
        print('The board is full and no one wins.  Thank you for playing!')
    else:
        # Someone won!
        print(f'Player {who_won} wins.  Congratulations!!!')

def board_check_regression_test(width=BOARD_WIDTH, height=BOARD_HEIGHT):
    board = make_board()

    board[board_xy_to_ind(5,2)] = 1
    board[board_xy_to_ind(4,2)] = 1
    board[board_xy_to_ind(3,2)] = 1
    board[board_xy_to_ind(2,2)] = 1

    print_board(board)
    cur_player = 1
    start_row = 4
    start_col = 2

    if has_player_won(start_row,start_col,cur_player,board):
        print('Test passed.')
    else:
        print('Test failed.')

def get_computer_settings():
    # Determine which players are the played by the computer and their intelligence levels.
    comp_player_vec = []
    for player in ['one','two']:
        while(True):
            str = input(f'Would you like player {player} to be played by the computer?  (Y/N) ').lower().strip()
            if str == 'n':
                comp_player_vec.append(HUMAN_PLAYER)
                break
            if str == 'y':
                while(True):
                    str = input(f'The computer\' intelligence may be as low as {MIN_INTELLIGENCE} or as high as {MAX_INTELLIGENCE}.  What would you like it to be? ')
                    try:
                        level = int(str)
                        if level >= MIN_INTELLIGENCE and level <= MAX_INTELLIGENCE:
                            comp_player_vec.append(level)
                            break
                    except:
                        # Do nothing.
                        str = ''

                    print('\n\t*** Invalid entry.  Please try again.\n')

                break

            print('\n\t*** Invalid entry.  Please try again.\n')

    return comp_player_vec

def run_connect_four():
    # Start a game

    # Determine which players are the computer and their intelligence levels.
    comp_player_vec = get_computer_settings()

    # Play the game.
    while (True):
        play_connect_four(comp_player_vec)

        # Determine if the player wishes to play another game.
        while(True):
            print('')
            str = input('Play another game (Y/N)? ').lower().strip()

            if str == 'y':
                break
            if str == 'n':
                print('\nThank you for playing!!!')
                return

            print('   *** Invalid entry.  Try again.')

run_connect_four()

#board_check_regression_test()
