"""Hexapawn Solver for CS442P at Portland state university.

:author: Kevin Midkiff
"""

import sys

BLACK_PIECE = 'p'
WHITE_PIECE = 'P'
EMPTY = '.'


def get_legal_moves(turn, posn):
    """Get the list legal moves from the current board position.
    """
    return None


def get_next_turn(turn):
    """Get whose next turn it is.
    """
    if turn == BLACK_PIECE:
        return WHITE_PIECE
    else:
        return BLACK_PIECE


def posn_value(turn, posn):
    """Get the next position value.
    """
    # Get the list of legal moves from my current position
    moves = get_legal_moves(turn, posn)

    # If there are no moves, then we have lost
    if moves is None:
        return -1

    # Assume loss
    max_val = -1

    # Iterate over all possible moves
    for m in moves:
        posn_p, result = m(posn)

        if result:
            val = -1
        else:
            val = - posn_value(get_next_turn(turn), posn_p)

        max_val = max(max_val, val)

        if max_val == 1:
            break

    return max_val


def main():
    board = []

    lines = sys.stdin.readlines()
    turn = lines[0].strip('\n')

    for line in lines[1:]:
        board.append(list(line.strip('\n')))

    print(turn)
    print(board)


if __name__ == '__main__':
    main()

