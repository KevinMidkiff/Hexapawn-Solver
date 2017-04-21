CS442 Assignment 2: Hexapawn Solver
===================================
> **Name:** Kevin Midkiff  
> **Email:** kmidkiff@pdx.edu

The purpose of this assignment a solver for the Hexapawn game developed by
Martin Gardner. In this game you have an m x n board with pawns on either side
of the board. Each player, white and black, has n number of pawns. The goal of
this game is to either block your opponent from being able to make any more moves,
or get one of your pawns to the other teams side and get a queen promotion, at
which point you've won the game.

This solver takes in a state of a board, i.e. could be the starting position of a game
or at any other point in the game, and figures out who, with perfect play on both sides,
will win the game. The algorithm I used for solving this problem is shown below.

```
find_winner(board)
    ##
    ## Input: representation of the current board state containing whose turn it is and the
    ##        the current state of the board itself.
    ## Output: -1 if it represents a loss for the player's whose turn it is or 1 if it from
    ##         current state the player whose turn it is will win
    ##
    moves <- get the possible legal moves from the current board state
    
    if there are no moves
        return -1  # i.e. I lost
    
    max_val = -1
    
    for m in move
        Execute the move
        result <- m(board)
        
        if result == true:
            val = 1
        else
            switch whose turn it is and call find_winner with board
            val = find_winner(board)
            switch the turn back to my turn, to maintain the state
        
        Undo the move that was taken to maintain the board state for check the next legal move
        
        max_val = max of the current value in max_val and val
        
        if max_val == 1
            break out of the for loop, because there is no need to analyze any more moves
    
    return max_val
```

The above algorithm is based off of the pseudo code discussed in class. It also takes advantage of
both the do-undo and win-parsing tactics. To implement this algorithm I choose to use the Python
programming language. In my code I have 1 object called Board. This object represents the current state
of the game, i.e. whose turn it is and the current state of the board. The board itself is a two-dimensional
array, where each row list contains an ASCII character representing the current value in that cell.
These ASCII characters are a, ".", for an empty cell, and, "p", for a black piece and, "P", for a white
piece. The Board object also handles checking if a piece at position (x0, y0) can be moved to the position
at (x1, y1). In addition, it also implements the executing of a move and the undoing of the same move.

The next main piece of the code is the finding of legal moves from a specific state. To do this I used the
following algorithm.

```
get_legal_moves(board)
    ##
    ## Input: Board representing the current board's state and whose move it is
    ## Output: List of available moves for the current player
    ##
    
    moves <- empty list
    
    for each cell in the board
        if the cell contains my piece (i.e. p for black or P for white)
            if I can capture a piece to my left
                append the move to the moves list
            if I can capture a piece to my right
                append the move to the moves list
            if I can move my piece straight ahead (i.e. I am not block by my opponent's piece)
                append the move to the list
    
    return moves
```

The tests included are in the positions directory, as well as in the tests directory. To run this
code you must have Python 3 or PyPy installed. It is recommended that you use PyPy as this will get better
performance over the normal Python 3 interpreter. The commands below show the execution of the Python script
and the result of the test which it is handed.

```sh
$ pypy hexapawn.py < tests/test1-in.txt
1
```

I would like to thank Eli Cook for the help he gave through discussion of strategies and help with debugging
this program.
