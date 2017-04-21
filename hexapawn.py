"""Hexapawn Solver for CS442P at Portland state university.

Thanks for Eli Cook for brainstorming design, and working through
bugs.

:author: Kevin Midkiff
"""
import sys


# Globals which represent the static characters which
# represent the board.
WHITE_TURN = 'W'
BLACK_TURN = 'B'
BLACK_PIECE = 'p'
WHITE_PIECE = 'P'
EMPTY = '.'


class Board:
    """Representation of the board.
    """
    def __init__(self, board, init_turn):
        """Constructor

        Arguments:
            board     - Multi-dimensional array of characters representing
                        a board's state.
            init_turn - Character representing whose turn it is, i.e. W or B
        """
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

        if init_turn == WHITE_TURN:
            self.turn = True
        else:
            self.turn = False

    def __str__(self):
        """Returns string for the ASCII representation of the board.
        """
        turn = BLACK_TURN
        if self.turn:
            turn = WHITE_TURN
        return "{}\n{}".format(turn, '\n'.join([''.join(i) for i in self.board]))

    def switch_turn(self):
        """Switch whose turn it is.
        """
        self.turn = not self.turn

    def check_place(self, x, y, x_offset, y_offset, dest_cell):
        """Check if the piece that is in cell (x,y) can be placed in the cell (x + x_offset, y + y_offset).
        dest_cell represents what the destination cell should be for the placement to be possible.
        For example, if you are looking to capture a piece at the destination cell, then dest_cell
        should be the type of your opponents piece, i.e. P or p.

        Arguments:
            x         - Source cell x coordinate
            y         - Source cell y coordinate
            x_offset  - Offset from x to destination's x coordinate
            y_offset  - Offset from y to destination's y coordinate
            dest_cell - Desired value in the destination cell
        """
        # Checking the user's input
        assert x < 0 or y < 0 or x < self.cols or y < self.rows, "Invalid (x,y) to place"

        piece = self.board[y][x]

        # Verify that we are not trying to check if an empty cell can be moved
        assert piece != EMPTY, "Cell asking to place from is empty"

        # Calculate the destination cell's (x,y)
        dest_x = x + x_offset
        dest_y = y + y_offset

        if dest_x < 0 or dest_y < 0:
            return False
        if dest_x >= self.cols or dest_y >= self.rows:
            return False

        return self.board[dest_y][dest_x] == dest_cell

    def move(self, posn, posn_next, undo):
        """Execute a move of the piece in cell posn to the cell posn_next. If the
        undo flag is set, then undo the move that was previously taken from posn to
        posn_next.
        """
        if undo:
            # If we are undoing, then swap posn and posn_next (since we are now going
            # backwards), then figure out what the new_cell should be, i.e. if we
            # previously captured a pawn, then we should replace that pawn
            tmp = posn
            posn = posn_next
            posn_next = tmp

            if posn[0] == posn_next[0]:
                new_cell = EMPTY
            elif self.turn:
                new_cell = BLACK_PIECE
            else:
                new_cell = WHITE_PIECE
        else:
            new_cell = EMPTY

        # Swap the values, and put the specified value into the posn cell
        cell = self.board[posn[1]][posn[0]]
        self.board[posn_next[1]][posn_next[0]] = cell
        self.board[posn[1]][posn[0]] = new_cell

        # Check if we have won by promoting a pawn to a queen
        if self.turn:
            # Check if white won by promotion
            return not undo and posn_next[1] == 0
        else:
            # Check if black won by promotion
            return not undo and posn_next[1] == (self.rows - 1)


def block_offsets(multi=1):
    """Get the offsets to check if a cell is blocked. Specify multi as -1
    if you want to check from white's position.

    Returns: Single value for y's offset (x's offset is always 0)
    """
    return multi * 1


def capture_offsets(multi=1):
    """get the offsets for check if we can capture left or right. Set multi to
    -1 if you want to check from white's position.

    Returns: Two tuples, with the first being the (x,y) offset for capturing left,
             and the second tuple being the (x,y) offset for capturing right.
    """
    return multi * -1, multi * 1, multi* 1, multi * 1


def base_move(x, y, x_offset, y_offset):
    """Base move method which returns a method to execute the move on the
    board that is passed into the method.
    """
    def do_move(board, undo=False):
        return board.move((x, y), (x + x_offset, y + y_offset), undo)

    return do_move


def get_legal_moves(board):
    """Get the list legal moves from the current board position.
    """
    moves = []

    if board.turn:
        # Set needed variables for getting legal moves when it is white's turn
        piece = WHITE_PIECE
        op_piece = BLACK_PIECE
        blk_y_off = block_offsets(-1)
        cap_lt_x_off, cap_lt_y_off, cap_rt_x_off, cap_rt_y_off = capture_offsets(-1)
    else:
        # Set needed variables for getting legal moves when it is black's turn
        piece = BLACK_PIECE
        op_piece = WHITE_PIECE
        blk_y_off = block_offsets()
        cap_lt_x_off, cap_lt_y_off, cap_rt_x_off, cap_rt_y_off = capture_offsets()

    for y in range(board.rows):
        for x in range(board.cols):
            col = board.board[y][x]
            if col == piece:
                # If I can capture to the left
                if board.check_place(x, y, cap_lt_x_off, cap_lt_y_off, op_piece):
                    moves.append(base_move(x, y, cap_lt_x_off, cap_lt_y_off))
                # If I can capture to the right
                if board.check_place(x, y, cap_rt_x_off, cap_rt_y_off, op_piece):
                    moves.append(base_move(x, y, cap_rt_x_off, cap_rt_y_off))
                # If can place in front
                if board.check_place(x, y, 0, blk_y_off, EMPTY):
                    moves.append(base_move(x, y, 0, blk_y_off))

    return moves


def find_winner(board):
    """Recursively find who wins the game assuming perfect play.
    """
    # Get the list of legal moves from my current position
    moves = get_legal_moves(board)

    # If there are no moves, then we have lost
    if not moves:
        return -1

    # Assume loss
    max_val = -1

    # Iterate over all possible moves
    for m in moves:
        # Execute the move and check if we've won as a result of that move
        if m(board):
            val = 1
        else:
            # If we haven't won, switch turns and try to find the winner at
            # the next level of the recursion
            board.switch_turn()
            val = - find_winner(board)
            # Switch turn back to my turn so future actions on the board are
            # done correctly
            board.switch_turn()

        # Undo the move we just tried
        m(board, undo=True)

        # Check if the new value is greater than the previous max value
        max_val = max(max_val, val)
        # Quick trying new moves if we've won
        if max_val == 1:
            break

    return max_val


def main():
    board = []
    lines = sys.stdin.readlines()
    turn = lines[0].strip('\n')

    for line in lines[1:]:
        board.append(list(line.strip('\n')))

    b = Board(board, turn)
    print(find_winner(b))


if __name__ == '__main__':
    main()

