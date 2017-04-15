"""Hexapawn Solver for CS442P at Portland state university.

:author: Kevin Midkiff
"""

import sys


WHITE_TURN = 'W'
BLACK_TURN = 'B'
BLACK_PIECE = 'p'
WHITE_PIECE = 'P'
EMPTY = '.'


class Board:
    """Representation of the board.
    """
    def __init__(self, board, init_turn):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

        if init_turn == WHITE_TURN:
            self.turn = True
        else:
            self.turn = False

    def __str__(self):
        turn = BLACK_TURN
        if self.turn:
            piece = WHITE_TURN
        return "{}\n{}".format(turn, '\n'.join([''.join(i) for i in self.board]))

    def switch_turn(self):
        """Switch whose turn it is.
        """
        self.turn = not self.turn

    def check_place(self, x, y, x_offset, y_offset, dest_cell):
        """Check if piece that is in cell (x,y) can be placed in cell (x + x_offset, y + y_offset).
        dest_cell represents what the destination cell should be for the placement to be possible.
        For example, if you are looking to capture a piece at the destination cell, then dest_cell
        should be the type of your opponents piece.

        Arguments:
            x         - Source cell x coordinate
            y         - Source cell y coordinate
            x_offset  - Offset from x to destination's x coordinate
            y_offset  - Offset from y to destination's y coordinate
            dest_cell - Desired value in the destination cell
        """
        # Checking the user's input
        assert(x > 0 and y > 0 and x < self.cols and y < self.rows, "Invalid (x,y) to place")

        piece = self.board[y][x]

        assert(piece != EMPTY, "Cell asking to place from is empty")

        dest_x = x + x_offset
        dest_y = y + y_offset

        if dest_x < 0 or dest_y < 0:
            return False
        if dest_x >= self.cols or dest_y >= self.rows:
            return False

        return self.board[dest_y][dest_x] == dest_cell

    def move(self, posn, posn_next, dest_cell, undo):
        """Execute a move of the piece in cell (x, y) to the cell (x + x_offset, y + y_offset).
        """
        if undo:
            tmp = posn
            posn = posn_next
            posn_next = tmp

        cell = self.board[posn[1]][posn[0]]
        self.board[posn_next[1]][posn_next[0]] = cell

        if dest_cell != EMPTY:
            self.board[posn[1]][posn[0]] = EMPTY
        else:
            self.board[posn[1]][posn[0]] = dest_cell


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
    return 1, multi * 1, -1, multi * 1


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
        for x in range(board.cols) :
            col = board.board[y][x]
            if col == piece:
                # If can place in front
                if board.check_place(x, y, 0, blk_y_off, EMPTY):
                    moves.append(lambda board, undo=False: board.move((x, y,), (x, y + blk_y_off,), EMPTY, undo))
                # If there I can capture to the left
                if board.check_place(x, y, cap_lt_x_off, cap_lt_y_off, op_piece):
                    moves.append(lambda board, undo=False: board.move((x, y,), (x + cap_lt_x_offset, y + cap_lt_y_offset,), op_piece, undo))
                # If I can capture to the right
                if board.check_place(x, y, cap_rt_x_off, cap_rt_y_off, op_piece):
                    moves.append(lambda board, undo=False: board.move((x, y,), (x + cap_rt_x_off, y + cap_rt_y_off,), op_piece, undo))

    return moves


def posn_value(board):
    """Get the next position value.
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
        # board_p, result = m(board)
        m(board)

        print(board)

        val = - posn_value(board)
        max_val = max(max_val, val)

        m(board, undo=True)

        if max_val == 1:
            break

        print(board)

    return max_val


def main():
    board = []

    lines = sys.stdin.readlines()
    turn = lines[0].strip('\n')

    for line in lines[1:]:
        board.append(list(line.strip('\n')))

    b = Board(board, turn)
    print(posn_value(b))


if __name__ == '__main__':
    main()

