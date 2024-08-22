# Author:           Eva Griffin
# GitHub username:  evacgriffin
# Description:      This project is an implementation of the falcon-hunter chess variant.
#
#                   Special rules: There is no check or checkmate, no castling, no en passant, no pawn promotion.
#                   If a player's king is captured, the game ends, and that player loses.
#
#                   Falcon: moves forward like a bishop, and backward like a rook
#                   Hunter: moves forward like a rook, and backward like a bishop
#                   Falcon and hunter start in the player's reserve, off the board. Once a player loses their queen,
#                   a rook, a bishop, or a knight, they may enter their falcon or hunter (on any subsequent move).
#                   These fairy pieces must enter play on any empty square of the player's two home ranks. Entering a
#                   fairy piece constitutes that player's turn. A player is eligible to enter their second fairy piece
#                   anytime after losing a second piece (queen, rook, bishop, or knight).
#
#                   Label conventions: Pieces are labeled using uppercase and lowercase characters.
#                   White pieces have an uppercase label. For example, the white queen is labeled 'Q'.
#                   Black pieces have a lowercase label. For example, a black pawn is labeled 'p'.

import unittest


class ChessPiece:
    """
    Represents a chess piece with a color and label.
    Responsible for keeping track of a chess piece's team color (black or white) and its label (to distinguish the
    type of chess piece).
    Has various child classes for each type of chess piece.
    """
    def __init__(self, color, label):
        """
        Creates a new ChessPiece object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        self._color = color

        # If the piece is white, we change the label to an uppercase char
        if color == 'white':
            self._label = label.upper()
        else:
            self._label = label

    def get_color(self):
        """
        Returns the chess piece's color.
        :return: color as a string, 'white' or 'black'
        """
        return self._color

    def get_label(self):
        """
        Returns the chess piece's label.
        :return: Label as a char
        """
        return self._label

    def diagonal_move_requires_jump(self, start_square, goal_square, board):
        """
        Checks whether other pieces are in the way of a proposed diagonal move (if a move requires a jump).
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    True if the move requires a jump
                    False if move doesn't require a jump
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Top right direction
        if goal_row > start_row and goal_column > start_column:
            current_column = ord(start_square[0]) + 1
            current_row = int(start_square[1]) + 1
            while current_row <= 8 or current_column <= ord('h'):
                current_square = chr(current_column) + str(current_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False

                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_row += 1
                current_column += 1

        # Bottom right direction
        if goal_row < start_row and goal_column > start_column:
            current_column = ord(start_square[0]) + 1
            current_row = int(start_square[1]) - 1
            while current_row >= 1 or current_column <= ord('h'):
                current_square = chr(current_column) + str(current_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False

                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_row -= 1
                current_column += 1

        # Top left direction
        if goal_row > start_row and goal_column < start_column:
            current_column = ord(start_square[0]) - 1
            current_row = int(start_square[1]) + 1
            while current_row <= 8 or current_column >= ord('a'):
                current_square = chr(current_column) + str(current_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False

                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_row += 1
                current_column -= 1

        # Bottom left direction
        if goal_row < start_row and goal_column < start_column:
            current_column = ord(start_square[0]) - 1
            current_row = int(start_square[1]) - 1
            while current_row >= 1 or current_column >= ord('a'):
                current_square = chr(current_column) + str(current_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False

                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_row -= 1
                current_column -= 1

    def straight_move_requires_jump(self, start_square, goal_square, board):
        """
        Checks whether other pieces are in the way of a proposed up/down or left/right move (if a move requires a jump).
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    True if the move requires a jump
                    False if move doesn't require a jump
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Up direction
        if goal_row > start_row:
            current_row = start_row + 1
            while current_row <= 8:
                current_square = start_column + str(current_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False

                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_row += 1

        # Down direction
        if goal_row < start_row:
            current_row = start_row - 1
            while current_row >= 1:
                current_square = start_column + str(current_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False
                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_row -= 1

        # Left direction
        if goal_column < start_column:
            current_column = ord(start_column) - 1
            while current_column >= ord('a'):
                current_square = chr(current_column) + str(start_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False

                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_column -= 1

        # Right direction
        if goal_column > start_column:
            current_column = ord(start_column) + 1
            while current_column <= ord('h'):
                current_square = chr(current_column) + str(start_row)
                # If we reach the goal square, the move did not require any jumps
                if current_square == goal_square:
                    return False
                # If we encounter another piece, the move requires a jump
                if board.get_current_piece_on_square(current_square) is not None:
                    return True
                current_column += 1


class Pawn(ChessPiece):
    """
    Represents a pawn chess piece with a color and label.
    Responsible for ensuring that a pawn can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    Communicates with the Board class to check for opposing chess pieces in diagonal forward directions.
    """
    def __init__(self, color, label='p'):
        """
        Creates a new Pawn object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)
        self._first_move = True  # Whether this is the pawn's first move

    def move_legal(self, start_square, goal_square, board):
        """
        Check if a proposed move is legal according to the pawn's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Check movement on first turn
        if self._first_move is True:
            # Don't allow moving forward more than 2 spaces
            if abs(goal_row - start_row) > 2:
                print("Pawns cannot move more than 2 spaces forward on their first turn!\n")
                return False
            # Don't allow jumping over another piece
            if goal_column == start_column and self.straight_move_requires_jump(start_square, goal_square, board):
                print("Pawns cannot jump over other pieces.\n")
                return False

        # Don't allow moving backwards or sideways
        if ((self._color == 'white' and goal_row < start_row)
                or (self._color == 'black' and goal_row > start_row)):
            print("Pawns cannot move backwards!\n")
            return False
        if goal_row == start_row:
            print("Pawns cannot move sideways!\n")
            return False

        # Check forward movement after the first turn
        if self._first_move is False:
            if goal_column == start_column and abs(goal_row - start_row) > 1:
                print("Pawns cannot move more than 1 space forward after their first turn!\n")
                return False

        # Get object on goal square to check if diagonal moves are allowed
        piece_on_goal_square = board.get_current_piece_on_square(goal_square)

        # Don't allow moving straight forward onto a square with another piece
        if start_column == goal_column and piece_on_goal_square is not None:
            print("Pawns cannot move straight forward to an occupied square.\n")
            return False

        # Don't allow diagonal movement to columns more than 1 square away
        if abs(ord(start_column) - ord(goal_column)) > 1:
            print("Pawns cannot move more than one square diagonally.\n")
            return False
        # Don't allow diagonal movement to empty squares
        if abs(ord(start_column) - ord(goal_column)) == 1 and piece_on_goal_square is None:
            print("Pawns cannot move diagonally to an empty square.\n")
            return False

        # If we get to this point, the proposed move is legal
        # If it's the pawn's first move, set first move to False and return
        if self._first_move is True:
            self._first_move = False

        return True


class Knight(ChessPiece):
    """
    Represents a knight chess piece with a color and label.
    Responsible for ensuring that a knight can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color, label='k'):
        """
        Creates a new Knight object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)

    def move_legal(self, start_square, goal_square):
        """
        Check if a proposed move is legal according to the knight's moveset.
        Knights are allowed to jump over other pieces.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Can move one square left or right and two squares up or down
        if abs(ord(goal_column) - ord(start_column)) == 1 and abs(goal_row - start_row) == 2:
            return True

        # Can move two squares left or right and one square up or down
        if abs(ord(goal_column) - ord(start_column)) == 2 and abs(goal_row - start_row) == 1:
            return True

        # Otherwise, the move is not legal
        print("The knight can only move in a 2+1 or 1+2 L shape!\n")
        return False


class Bishop(ChessPiece):
    """
    Represents a bishop chess piece with a color and label.
    Responsible for ensuring that a bishop can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color, label='b'):
        """
        Creates a new Bishop object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)

    def move_legal(self, start_square, goal_square, board):
        """
        Check if a proposed move is legal according to the bishop's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # We must check that we move the same number horizontally as vertically to reach goal square
        if abs(ord(goal_column)-ord(start_column)) != abs(goal_row-start_row):
            print("Bishops can only move diagonally!\n")
            return False

        # If the proposed move requires a jump, the move is illegal
        if self.diagonal_move_requires_jump(start_square, goal_square, board):
            print("Bishops cannot jump over other pieces!\n")
            return False
        else:
            # Otherwise, no jumps are required and the proposed move is legal
            return True


class Rook(ChessPiece):
    """
    Represents a rook chess piece with a color and label.
    Responsible for ensuring that a rook can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color, label='r'):
        """
        Creates a new Rook object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)

    def move_legal(self, start_square, goal_square, board):
        """
        Check if a proposed move is legal according to the rook's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Is goal_square on the same column or row as start_square?
        if ord(goal_column) != ord(start_column) and goal_row != start_row:
            print("Rooks can only move horizontally or vertically!\n")
            return False

        # If the proposed move requires a jump, the move is illegal
        if self.straight_move_requires_jump(start_square, goal_square, board):
            print("Rooks cannot jump over other pieces!\n")
            return False
        else:
            # Otherwise, no jumps are required and the proposed move is legal
            return True


class Queen(ChessPiece):
    """
    Represents a queen chess piece with a color and label.
    Responsible for ensuring that a queen can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color, label='q'):
        """
        Creates a new Queen object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)

    def move_legal(self, start_square, goal_square, board):
        """
        Check if a proposed move is legal according to the queen's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # We must check that we move either diagonally or straight up/down/left/right
        if abs(ord(goal_column) - ord(start_column)) != abs(goal_row - start_row):
            if ord(goal_column) != ord(start_column) and goal_row != start_row:
                print("A queen can only move diagonally, or straight up, down, left or right!\n")
                return False

        # If a proposed diagonal move requires a jump, the move is illegal
        if abs(ord(goal_column) - ord(start_column)) == abs(goal_row - start_row):
            if self.diagonal_move_requires_jump(start_square, goal_square, board):
                print("A queen cannot jump over other pieces!\n")
                return False

        # If a proposed straight move requires a jump, the move is illegal
        if ord(goal_column) == ord(start_column) or goal_row == start_row:
            if self.straight_move_requires_jump(start_square, goal_square, board):
                print("A queen cannot jump over other pieces!\n")
                return False
        else:
            # Otherwise, no jumps are required and the proposed move is legal
            return True


class King(ChessPiece):
    """
    Represents a king chess piece with a color and label.
    Responsible for ensuring that a king can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color, label='g'):
        """
        Creates a new King object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)

    def move_legal(self, start_square, goal_square):
        """
        Check if a proposed move is legal according to the king's moveset.
        Since a king can only move one space in each direction, we do not have to check for jumps.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Move is illegal if goal square is more than one square away from start square
        if abs(ord(goal_column) - ord(start_column)) > 1 or abs(goal_row - start_row) > 1:
            print("A king can only move one square in any direction!\n")
            return False
        else:
            # Otherwise, the proposed move is legal
            return True


class Falcon(ChessPiece):
    """
    Represents a falcon chess piece with a color and label.
    Responsible for ensuring that a falcon can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color, label='f'):
        """
        Creates a new Falcon object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)

    def move_legal(self, start_square, goal_square, board):
        """
        Check if a proposed move is legal according to the falcon's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Falcon's cannot move straight left or right
        if start_row == goal_row:
            print("Falcons cannot move straight left or right!\n")
            return False

        # Checks for white pieces
        if self._color == 'white':
            # If we are trying to move backwards, but not within the same column, the move is illegal
            if goal_row < start_row and ord(goal_column) != ord(start_column):
                print("Falcons can only move straight backwards!\n")
                return False
            # If we are trying to move forward, but not on a diagonal, the move is illegal
            elif goal_row > start_row and abs(ord(goal_column)-ord(start_column)) != abs(goal_row-start_row):
                print("Falcons can only move diagonally forward!\n")
                return False

            # If we are trying to move backwards, we must check for jumps in that direction
            if goal_row < start_row:
                # If a proposed straight move requires a jump, the move is illegal
                if self.straight_move_requires_jump(start_square, goal_square, board):
                    print("A falcon cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True
            # If we are trying to move diagonally, we must check for jumps in that direction
            elif goal_row > start_row:
                # If a proposed diagonal move requires a jump, the move is illegal
                if self.diagonal_move_requires_jump(start_square, goal_square, board):
                    print("A falcon cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True

        # Checks for black pieces
        if self._color == 'black':
            # If we are trying to move backwards, but not within the same column, the move is illegal
            if goal_row > start_row and ord(goal_column) != ord(start_column):
                print("Falcons can only move straight backwards!\n")
                return False
            # If we are trying to move forward, but not on a diagonal, the move is illegal
            elif goal_row < start_row and abs(ord(goal_column) - ord(start_column)) != abs(goal_row - start_row):
                print("Falcons can only move diagonally forward!\n")
                return False

            # If we are trying to move backwards, we must check for jumps in that direction
            if goal_row > start_row:
                # If a proposed straight move requires a jump, the move is illegal
                if self.straight_move_requires_jump(start_square, goal_square, board):
                    print("A falcon cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True
            # If we are trying to move diagonally, we must check for jumps in that direction
            elif goal_row < start_row:
                # If a proposed diagonal move requires a jump, the move is illegal
                if self.diagonal_move_requires_jump(start_square, goal_square, board):
                    print("A falcon cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True


class Hunter(ChessPiece):
    """
    Represents a hunter chess piece with a color and label.
    Responsible for ensuring that a hunter can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by ChessVar instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color, label='h'):
        """
        Creates a new Hunter object with the specified color and label.
        :param color: 'black' or 'white' as a string
        :param label: piece label as a lowercase char
        """
        super().__init__(color, label)

    def move_legal(self, start_square, goal_square, board):
        """
        Check if a proposed move is legal according to the hunter's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        start_column = start_square[0]
        start_row = int(start_square[1])
        goal_column = goal_square[0]
        goal_row = int(goal_square[1])

        # Hunter's cannot move straight left or right
        if start_row == goal_row:
            print("Hunters cannot move straight left or right!\n")
            return False

        # Checks for white pieces
        if self._color == 'white':
            # If we are trying to move forward, but not within the same column, the move is illegal
            if goal_row > start_row and ord(goal_column) != ord(start_column):
                print("Hunters can only move straight forward!\n")
                return False
            # If we are trying to move backward, but not on a diagonal, the move is illegal
            elif goal_row < start_row and abs(ord(goal_column)-ord(start_column)) != abs(goal_row-start_row):
                print("Hunters can only move diagonally backward!\n")
                return False

            # If we are trying to move forward, we must check for jumps in that direction
            if goal_row > start_row:
                # If a proposed straight move requires a jump, the move is illegal
                if self.straight_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True
            # If we are trying to move backward, we must check for jumps in that direction
            elif goal_row < start_row:
                # If a proposed diagonal move requires a jump, the move is illegal
                if self.diagonal_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True

        # Checks for black pieces
        if self._color == 'black':
            # If we are trying to move forward, but not within the same column, the move is illegal
            if goal_row < start_row and ord(goal_column) != ord(start_column):
                print("Hunters can only move straight forward!\n")
                return False
            # If we are trying to move backward, but not on a diagonal, the move is illegal
            elif goal_row > start_row and abs(ord(goal_column) - ord(start_column)) != abs(
                    goal_row - start_row):
                print("Hunters can only move diagonally backward!\n")
                return False
            # If we are trying to move forward, we must check for jumps in that direction
            if goal_row < start_row:
                # If a proposed straight move requires a jump, the move is illegal
                if self.straight_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True
            # If we are trying to move backward, we must check for jumps in that direction
            elif goal_row > start_row:
                # If a proposed diagonal move requires a jump, the move is illegal
                if self.diagonal_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False
                else:
                    # Otherwise, no jumps are required and the proposed move is legal
                    return True


class Board:
    """
    Represents a standard 8x8 chess board where the rows are labeled with numbers 1-8 and the columns are labeled with
    letters a-h.
    Responsible for initializing and storing the current layout of the chess board, printing out a visualization of the
    current board layout, and completing a move by updating the two relevant squares on the board after a move has been
    validated by the ChessVar class.
    Needs to communicate with the ChessPiece class (and its various child classes) since these pieces can be present on
    the board. Also communicates with the ChessVar class to update its layout when needed.
    """
    def __init__(self):
        """
        Creates a new Board object.
        The chess board is represented by a list of dictionaries.
        Each row is a dictionary, where the keys are the square labels and the values are ChessPiece objects
        If a square on the board is empty, its value is None
        """
        self._layout = [
            {'a8': Rook('black'), 'b8': Knight('black'), 'c8': Bishop('black'), 'd8': Queen('black'),
             'e8': King('black'), 'f8': Bishop('black'), 'g8': Knight('black'), 'h8': Rook('black')},

            {'a7': Pawn('black'), 'b7': Pawn('black'), 'c7': Pawn('black'), 'd7': Pawn('black'),
             'e7': Pawn('black'), 'f7': Pawn('black'), 'g7': Pawn('black'), 'h7': Pawn('black')},

            {'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None},

            {'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None},

            {'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None},

            {'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None},

            {'a2': Pawn('white'), 'b2': Pawn('white'), 'c2': Pawn('white'), 'd2': Pawn('white'),
             'e2': Pawn('white'), 'f2': Pawn('white'), 'g2': Pawn('white'), 'h2': Pawn('white')},

            {'a1': Rook('white'), 'b1': Knight('white'), 'c1': Bishop('white'), 'd1': Queen('white'),
             'e1': King('white'), 'f1': Bishop('white'), 'g1': Knight('white'), 'h1': Rook('white')}
        ]

    def get_current_piece_on_square(self, square):
        """
        Get the current chess piece on the specified square.
        :param square: square as a two character string label
        :return: ChessPiece object currently located on square, None if the square is empty
        """
        # Search for the specified square and return its associated chess piece
        for row in self._layout:
            for key, value in row.items():
                if key == square:
                    if value is None:
                        return None
                    else:
                        return value

    def print(self):
        """
        Prints out the current layout of the board.
        :return: No return value
        """
        # Print column labels at the top
        print('  ', end='')
        for val in range(97, 105):
            print(f" {chr(val)} ", end='')
        print('\n')

        curr_row = 8
        for row in self._layout:
            print(f"{curr_row} ", end='')
            for piece in row.values():
                # If there is no piece on the square, print an underscore character
                if piece is None:
                    print(' _ ', end='')
                # If there is a piece, print its label
                else:
                    print(f" {piece.get_label()} ", end='')
            # Move to next line
            print('\n')
            curr_row -= 1

        # Print column labels at the bottom
        print('  ', end='')
        for val in range(97, 105):
            print(f" {chr(val)} ", end='')
        print('\n\n')

    def update_move(self, start_square, goal_square, piece):
        """
        Update the current state of the board by updating start_square to None (the piece was moved away from this
        square) and goal_square to the specified piece (the piece was moved here).
        :param start_square: first square label as a two character string corresponding to dictionary key in the
        board's layout
        :param goal_square: second square label as a two character string corresponding to dictionary key in the
        board's layout
        :param piece: ChessPiece object to be placed on goal_square
        :return: No return value, the board layout is updated in place
        """
        for row in self._layout:
            for key in row.keys():
                # Find start_square and update its value to None
                if key == start_square:
                    row[key] = None
                # Find goal_square and update its value to the ChessPiece object
                if key == goal_square:
                    row[key] = piece

    def update_piece_entered(self, square, piece):
        """
        Update the current state of the board by entering the specified piece on the specified square.
        :param square: square label as a two character string
        :param piece: ChessPiece object to be placed on the specified square
        :return: No return value, the layout is updated in place
        """
        for row in self._layout:
            for key in row.keys():
                # Find square and update its value to piece
                if key == square:
                    row[key] = piece


class Player:
    """
    Represents a chess player.
    Responsible for keeping track of the player's team color (black or white), available fairy pieces, and previously
    captured pieces (to check if the player is allowed to enter a fairy piece).
    Communicates with ChessPiece class and its various child classes to keep track of fairy pieces and captured
    pieces.
    """
    def __init__(self, color):
        """
        Creates a new player object with the specified color.
        :param color: player color as a string, 'black' or 'white'
        """
        self._color = color
        # List of ChessPiece objects, represents player's available fairy pieces, starts with one falcon and one hunter
        self._fairy_pieces = [Falcon(self._color), Hunter(self._color)]
        # List of ChessPiece objects, represents player's pieces that have been captured by the other player during
        # previous turns, initially empty
        self._captured_pieces = []

    def get_fairy_pieces(self):
        """
        Returns the player's current list of available fairy pieces that can be entered into the game.
        :return: Python list of ChessPiece objects
        """
        return self._fairy_pieces

    def get_captured_pieces(self):
        """
        Returns a list of the pieces the player has lost in the game so far.
        :return: Python list of ChessPiece objects
        """
        return self._captured_pieces

    def add_captured_piece(self, captured_piece):
        """
        Adds the specified captured piece to the list of captured pieces for this player.
        :param captured_piece: the captured piece as a ChessPiece object
        :return: No return value, the list is changed in place
        """
        self._captured_pieces.append(captured_piece)

    def remove_fairy_piece(self, fairy_piece):
        """
        Remove the specified fairy piece from the player's list of available fairy pieces.
        :param fairy_piece: the entered fairy piece as a ChessPiece object
        :return: No return value, the list is changed in place
        """
        self._fairy_pieces.remove(fairy_piece)

    def print_fairy_pieces(self):
        """
        Prints out a list of the player's available fairy pieces.
        :return: No return value
        """
        for fairy_piece in self._fairy_pieces:
            print(fairy_piece)

    def print_captured_pieces(self):
        """
        Prints out a list of the player's pieces that have been captured by the other player on previous turns.
        :return: No return value
        """
        for captured_piece in self._captured_pieces:
            print(captured_piece)


class ChessVar:
    """
    Represents a falcon-hunter chess game with two players.
    Responsible for the overall game loop: initializing a chess board, initializing two players, setting which player's
    turn it is, and keeping track of the game state (whether the game is ongoing or which player won).
    ChessVar is also responsible for making a move and ensuring that the move is legal, as well as entering a fairy
    piece to the game if it's allowed.
    Communicates with the Board class to initialize and update the chess board, with the Player class to create and keep
    track of the two players, and the ChessPiece class (and its various child classes) to verify if moves are legal
    according to a piece's moveset.
    """
    def __init__(self):
        """
        Creates a new chess game object.
        """
        # Initialize the board.
        self._board = Board()

        # Initialize the two players.
        self._white = Player('white')
        self._black = Player('black')

        # White begins per the standard rules
        # Integer 1: White's turn, Integer -1: Black's turn
        # This way, to switch turns, all we have to do is multiply by (-1) to flip the value
        self._player_turn = 1

        # Initial game state
        # Other possible states are 'WHITE_WON' and 'BLACK_WON'
        self._game_state = 'UNFINISHED'

    def print_board(self):
        """
        Prints out the current state of the chess board.
        :return: No return value, prints out the board.
        """
        self._board.print()

    def get_game_state(self):
        """
        Returns the game's current state.
        :return: game state as a string
        """
        return self._game_state

    def get_player_turn(self):
        """
        Returns the value representing which player's turn it is.
        :return: player turn as an integer, 1 if it's White's turn, -1 if it's Black's turn
        """
        return self._player_turn

    def go_to_next_turn(self):
        """
        Changes the current turn to the other player.
        A value of 1 corresponds to player1 and a value of -1 corresponds to player2.
        :return: No return value, changes self._player_turn in place
        """
        self._player_turn *= (-1)

    def make_move(self, start_square, goal_square):
        """
        Moves a piece from start_square to goal_square.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :return:    Boolean:
                    False if move is illegal or game has already been won
                    True if move is legal
        """

        # Check if move is legal:
        # Is the game over?
        if self._game_state != 'UNFINISHED':
            print("The game is over! No more moves can be made!\n")
            return False

        # Is start_square = goal_square?
        if start_square == goal_square:
            print("Moving from a square to itself is an illegal move.\n")
            return False

        # Is goal_square within the bounds of the game board?
        # Board ranges: rows [1,8], columns [a,h]
        column = goal_square[0]
        row = int(goal_square[1])
        if column < 'a' or column > 'h':
            print("Column out of bounds! Cannot move chess piece off the board.\n")
            return False
        if row < 1 or row > 8:
            print("Row out of bounds! Cannot move chess piece off the board.\n")
            return False

        piece_on_start_square = self._board.get_current_piece_on_square(start_square)
        # Does start_square contain a chess piece at all?
        if piece_on_start_square is None:
            print("The specified start square does not contain a chess piece. Move cannot be completed.\n")
            return False

        # Does start_square contain a piece belonging to the current player?
        # If color is 'black' and player_turn = 1, move is illegal
        piece_on_start_square_color = piece_on_start_square.get_color()
        if piece_on_start_square_color == 'black' and self._player_turn == 1:
            print("It's white's turn! Cannot move a black chess piece.\n")
            return False

        # If color is 'white' and player_turn = -1, move is illegal
        if piece_on_start_square_color == 'white' and self._player_turn == -1:
            print("It's black's turn! Cannot move a white chess piece.\n")
            return False

        # Is the proposed move legal for this type of ChessPiece?
        if piece_on_start_square.get_label().lower() in ['k', 'g']:
            # Don't need to pass the board if it's a knight or a king
            if piece_on_start_square.move_legal(start_square, goal_square) is False:
                return False
        else:
            if piece_on_start_square.move_legal(start_square, goal_square, self._board) is False:
                return False

        # Does goal_square contain a piece from the current player?
        piece_on_goal_square = self._board.get_current_piece_on_square(goal_square)

        if piece_on_goal_square is not None:
            piece_on_goal_square_color = piece_on_goal_square.get_color()
            # If color is 'white' and player_turn = 1, move is illegal
            if piece_on_goal_square_color == 'white' and self._player_turn == 1:
                print("The goal square already contains a white chess piece!\n")
                return False

            # If color is 'black' and player_turn = -1, move is illegal
            if piece_on_goal_square_color == 'black' and self._player_turn == -1:
                print("The goal square already contains a black chess piece!\n")
                return False

            # If we reach this point, the proposed move is legal!

            # Does goal_square contain a piece? Capture it!
            # Add captured piece to that players list of captured pieces
            if piece_on_goal_square_color == 'white':
                self._white.add_captured_piece(piece_on_goal_square)
                print("Black captured a piece!\n")
                print("White's captured pieces: ", end=' ')
                for piece in self._white.get_captured_pieces():
                    print(piece.get_label(), end=' ')
                print('\n')
            elif piece_on_goal_square_color == 'black':
                self._black.add_captured_piece(piece_on_goal_square)
                print("White captured a piece!\n")
                print("Black's captured pieces: ", end=' ')
                for piece in self._black.get_captured_pieces():
                    print(piece.get_label(), end=' ')
                print('\n')

            # If the captured piece was a king, update the game state
            # If the black king was captured
            if piece_on_goal_square.get_label() == 'g':
                self._game_state = 'WHITE_WON'
                print("White has captured Black's king! White wins the game!\n")
            # If the white king was captured
            elif piece_on_goal_square.get_label() == 'G':
                self._game_state = 'BLACK_WON'
                print("Black has captured White's king! Black wins the game!\n")

        # Complete the move
        self._board.update_move(start_square, goal_square, piece_on_start_square)

        # Print out the updated board and go to next turn
        self._board.print()
        self.go_to_next_turn()
        return True

    def enter_fairy_piece(self, piece_type, square):
        """
        Enters the specified fairy piece into the game on the specified square.
        :param piece_type: fairy piece as a char
        :param square: square to place the piece on as a string
        :return:    Boolean:
                    False if the piece is not allowed to enter this square at this turn
                    True if the piece can enter the specified square legally
        """
        square_row = int(square[1])

        # Is the game over?
        if self._game_state != 'UNFINISHED':
            print("The game is over! No more fairy pieces can be entered!\n")
            return False

        # Obtain the list of fairy pieces available to the current player and the list
        # of previously captured pieces for that player
        if self._player_turn == 1:
            available_fairy_pieces = self._white.get_fairy_pieces()
            captured_pieces = self._white.get_captured_pieces()
        else:
            available_fairy_pieces = self._black.get_fairy_pieces()
            captured_pieces = self._black.get_captured_pieces()

        # Count the number of major pieces the current player has lost
        major_piece_labels = ['q', 'r', 'b', 'k']
        num_major_pieces = 0
        for piece in captured_pieces:
            if piece.get_label().lower() in major_piece_labels:
                num_major_pieces += 1

        # If this is the first time the current player is trying to enter a fairy piece,
        # but they haven't lost any major pieces yet, we cannot enter the fairy piece
        if len(available_fairy_pieces) == 2 and num_major_pieces == 0:
            print("This player cannot enter a fairy piece since they have not lost any major pieces yet!\n")
            return False
        elif len(available_fairy_pieces) == 1 and num_major_pieces == 1:
            print(
                "This player cannot enter a second fairy piece since they have not lost a second major piece yet!\n")
            return False

        piece_on_square = self._board.get_current_piece_on_square(square)
        # Does the specified square contain a chess piece already?
        if piece_on_square is not None:
            print("The specified square already contains a chess piece. The fairy piece cannot be entered there.\n")
            return False

        # Checks for white's turn
        if self._player_turn == 1:
            # Is the square outside of white's home ranks?
            if square_row > 2:
                print("White cannot enter a piece outside of row 1 or row 2!\n")
                return False
            # Is the specified piece label consistent with being a white chess piece?
            if piece_type != 'F' and piece_type != 'H':
                print("White cannot enter a black fairy piece!\n")
                return False
        # Checks for black's turn
        else:
            # Is the square outside of black's home ranks?
            if square_row < 7:
                print("Black cannot enter a piece outside of row 7 or row 8!\n")
                return False
            # Is the specified piece label consistent with being a black chess piece?
            if piece_type != 'f' and piece_type != 'h':
                print("Black cannot enter a white fairy piece!\n")
                return False

        # Does the current player have any fairy pieces available?
        if len(available_fairy_pieces) == 0:
            print("Sorry! This player doesn't have any fairy pieces left!\n")
            return False

        # If the specified piece available?
        fairy_piece = None
        # Search the available fairy pieces for the specified piece
        for piece in available_fairy_pieces:
            if piece_type == piece.get_label():
                fairy_piece = piece

        # If we couldn't find the specified piece, it's not available
        if fairy_piece is None:
            print("The current player does not have this type of fairy piece available anymore!\n")
            return False

        # If we get through all of the above checks, we can legally enter the fairy piece

        # Enter the fairy piece on the board at that position
        self._board.update_piece_entered(square, fairy_piece)

        # Remove the fairy piece from the current player's list of available fairy pieces
        if self._player_turn == 1:
            self._white.remove_fairy_piece(fairy_piece)
        else:
            self._black.remove_fairy_piece(fairy_piece)

        # Print out the updated board and go to next turn
        self._board.print()
        self.go_to_next_turn()
        return True


def main():
    print("Welcome to ChessVar, a falcon-hunter chess game!\n")
    print("Please enter squares in the following format: ColumnRow. Examples: a3, f8, h5.")
    print("White and black chess pieces are represented by upper-case and lower-case letters respectively "
          "(for example, 'P' for white pawn and 'b' for black bishop).\n")
    print("Each player has two fairy pieces on reserve: one hunter and one falcon.")
    print("Hunters move forward like a rook (straight) and backward like a bishop (diagonally).")
    print("Falcons move forward like a bishop (diagonally) and backward like a rook (straight).")
    print("A player may enter their first fairy piece on any turn after they have lost at least one major piece "
          "(queen, bishop, knight, or rook). A player may enter their second fairy piece on any turn after they have "
          "lost at least a second major piece.")
    print("Fairy pieces may only be entered on a square in one of the player's two home ranks.")
    print("Entering a fairy piece counts as the player's full turn.")
    print("If you'd like to enter a fairy piece, please do so in the following format:\n"
          "Enter the type of piece as a letter: f or h for the black falcon or hunter, F or H for the white falcon or "
          "hunter.\n")
    print("Let's begin! White gets to make the first move.\n")

    game = ChessVar()
    game.print_board()

    while game.get_game_state() == 'UNFINISHED':
        # Print current player
        if game.get_player_turn() == 1:
            print("White's turn!\n")
        else:
            print("Black's turn!\n")

        entering_fairy_piece = input("Would you like to enter a fairy piece? (y/n): ")
        if entering_fairy_piece == 'y':
            piece_type = input("What type of fairy piece would you like to enter? (f, F, h, H): ")
            square = input("Which square do you want to place the fairy piece on? ")
            game.enter_fairy_piece(piece_type, square)
        else:
            print("\nPlease make your move!\n")
        start_square = input("Start square: ")
        goal_square = input("Goal square: ")

        print(f"Moving from {start_square} to {goal_square}:\n")

        game.make_move(start_square, goal_square)

    if game.get_game_state() == 'BLACK_WON':
        winner = 'Black'
    else:
        winner = 'White'

    print(f"GAME OVER! {winner} won!\n")


if __name__ == '__main__':
    main()


# TEST CODE
# class TestChessVar(unittest.TestCase):
#     """Contains unit tests for the ChessVar class"""
#     def test_basic_make_move(self):
#         """Test basic functionality of the make_move() method."""
#         game = ChessVar()
#         self.assertFalse(game.make_move('c3', 'c4'))  # Attempt to make a move from an empty start square
#         self.assertFalse(game.make_move('f7', 'f5'))  # Attempt to move a piece that doesn't belong to the current player
#         self.assertFalse(game.make_move('g1', 'i2'))  # Attempt to move a piece to a column that isn't on the board
#         self.assertFalse(game.make_move('a1', 'Z1'))  # Attempt to move a piece to a column that isn't on the board
#         self.assertFalse(game.make_move('e1', 'e0'))  # Attempt to move a piece to a row that isn't on the board
#         self.assertFalse(game.make_move('g2', 'g9'))  # Attempt to move a piece to a row that isn't on the board
#         self.assertFalse(game.make_move('h1', 'g1'))  # Attempt to move a piece to a square that already contains a piece by the current player
#
#     def test_pawn_movement(self):
#         """Test pawn movement."""
#         game = ChessVar()
#         self.assertTrue(game.make_move('c2', 'c4'))  # White moves two squares fwd
#         self.assertTrue(game.make_move('d7', 'd5'))  # Black moves two squares fwd
#         self.assertTrue(game.make_move('c4', 'd5'))  # White captures the black pawn
#         self.assertFalse(game.make_move('h2', 'h3'))  # White tries to make another move
#         self.assertTrue(game.make_move('g7', 'g6'))  # Black moves one square fwd
#         self.assertTrue(game.make_move('f2', 'f4'))  # White moves two squares fwd
#         self.assertTrue(game.make_move('f7', 'f5'))  # Black moves two squares fwd
#         self.assertFalse(game.make_move('f4', 'f5'))  # White tries to capture by going straight fwd
#         self.assertTrue(game.make_move('e2', 'e4'))  # White moves two squares fwd
#         self.assertTrue(game.make_move('f5', 'e4'))  # Black captures a white pawn
#         self.assertFalse(game.make_move('f4', 'f3'))  # White tries to move a pawn backwards
#         self.assertTrue(game.make_move('a2', 'a3'))  # White moves pawn one square fwd
#         self.assertFalse(game.make_move('e4', 'e5'))  # Black tries to move a pawn backwards
#         self.assertTrue(game.make_move('e4', 'e3'))  # Black moves pawn one square fwd
#         self.assertTrue(game.make_move('b2', 'b4'))  # White moves pawn two squares fwd
#         self.assertFalse(game.make_move('e3', 'f4'))  # Black tries capturing backwards
#         self.assertTrue(game.make_move('g6', 'g5'))  # Black moves pawn one square fwd
#         self.assertTrue(game.make_move('d5', 'd6'))  # White moves pawn one square fwd
#         self.assertTrue(game.make_move('g5', 'g4'))  # Black moves pawn one square fwd
#         self.assertFalse(game.make_move('d6', 'c6'))  # White tries to move pawn one square sideways
#         self.assertTrue(game.make_move('d6', 'e7'))  # White captures a black pawn
#         self.assertTrue(game.make_move('g4', 'g3'))  # Black moves pawn one square fwd
#         self.assertTrue(game.make_move('e7', 'd8'))  # White captures black's queen
#         self.assertFalse(game.make_move('c7', 'd7'))  # Black tries to move pawn one square sideways
#         self.assertFalse(game.make_move('b7', 'a6'))  # Black tries to move pawn diagonally fwd onto an empty square
#         self.assertTrue(game.make_move('b7', 'b6'))  # Black moves pawn one square fwd
#         self.assertFalse(game.make_move('g2', 'g4'))  # White tries to jump over a black pawn
#         self.assertFalse(game.make_move('a3', 'a5'))  # White tries to move pawn two squares fwd when it is not the pawn's first turn
#         self.assertFalse(game.make_move('d2', 'd5'))  # White tries to move pawn more than two squares on first turn
#         self.assertFalse(game.make_move('b4', 'd6'))  # White tries to move pawn more than 1 space diagonally
#         self.assertTrue(game.make_move('d2', 'd3'))  # White moves pawn one square fwd
#         self.assertFalse(game.make_move('b6', 'b4'))  # Black tries to move pawn two squares fwd when it is not the pawn's first turn
#         self.assertFalse(game.make_move('h7', 'h4'))  # Black tries to move pawn more than two squares on first turn
#         self.assertFalse(game.make_move('c7', 'e5'))  # Black tries to move pawn more than 1 space diagonally
#         self.assertTrue(game.make_move('c7', 'c5'))  # Black moves pawn one square fwd
#
#     def test_knight_movement(self):
#         """Test knight movement."""
#         game = ChessVar()
#         self.assertTrue(game.make_move('b1', 'a3'))  # White moves a knight
#         self.assertTrue(game.make_move('g8', 'f6'))  # Black moves a knight
#         self.assertTrue(game.make_move('g1', 'f3'))  # White moves a knight
#         self.assertFalse(game.make_move('b8', 'b6'))  # Black tries to move a knight illegally
#         self.assertTrue(game.make_move('b8', 'a6'))  # Black moves a knight
#         self.assertFalse(game.make_move('a3', 'c2'))  # White tries to move a knight onto an occupied square
#         self.assertFalse(game.make_move('a3', 'd4'))  # White tries to move a knight illegally
#         self.assertTrue(game.make_move('a3', 'b5'))  # White moves a knight
#         self.assertTrue(game.make_move('a6', 'b4'))  # Black moves a knight and jumps over a white knight
#         self.assertTrue(game.make_move('b5', 'c7'))  # White moves a knight and captures a black pawn
#         self.assertTrue(game.make_move('b4', 'a2'))  # Black moves a knight and captures a white pawn
#         self.assertTrue(game.make_move('c7', 'e8'))  # White moves a knight and captures the black king
#         self.assertFalse(game.make_move('a2', 'c1'))  # Black attempts to make a move after white already won
#         self.assertEqual(game.get_game_state(), 'WHITE_WON')  # Test correct game state
#
#     def test_bishop_movement(self):
#         """Test bishop movement."""
#         game = ChessVar()
#         self.assertFalse(game.make_move('d7', 'd5'))  # Black attempts to move first
#         self.assertTrue(game.make_move('g2', 'g4'))  # White moves a pawn two squares fwd
#         self.assertTrue(game.make_move('d7', 'd5'))  # Black moves a pawn two squares fwd
#         self.assertTrue(game.make_move('f1', 'h3'))  # White moves a bishop
#         self.assertFalse(game.make_move('c8', 'a6'))  # Black attempts to make a bishop jump over a pawn
#         self.assertTrue(game.make_move('c8', 'g4'))  # Black moves a bishop and captures a white pawn
#         self.assertFalse(game.make_move('h3', 'h4'))  # White tries to move a bishop straight upwards
#         self.assertTrue(game.make_move('h3', 'g4'))  # White captures a black bishop
#         self.assertTrue(game.make_move('e7', 'e5'))  # Black moves a pawn two squares fwd
#         self.assertTrue(game.make_move('g4', 'c8'))  # White moves a bishop
#         self.assertTrue(game.make_move('f8', 'c5'))  # Black moves a bishop
#         self.assertFalse(game.make_move('c8', 'a6'))  # White tries to move a bishop by jumping over a black pawn
#         self.assertTrue(game.make_move('c8', 'e6'))  # White moves a bishop
#         self.assertFalse(game.make_move('c5', 'a5'))  # Black tries to move a bishop sideways
#         self.assertFalse(game.make_move('c5', 'a7'))  # Black tries to move a bishop to an occupied square
#         self.assertTrue(game.make_move('c5', 'f2'))  # Black captures a white pawn
#         self.assertFalse(game.make_move('e6', 'e8'))  # White tries to capture black's king with a bishop
#         self.assertTrue(game.make_move('e6', 'f7'))  # White captures a black pawn
#         self.assertTrue(game.make_move('f2', 'e1'))  # Black captures white's king
#         self.assertFalse(game.make_move('f7', 'g8'))  # White attempts to make a move after black already won
#         self.assertEqual(game.get_game_state(), 'BLACK_WON')  # Test correct game state
#
#     def test_rook_movement(self):
#         """Test rook movement."""
#         game = ChessVar()
#         self.assertTrue(game.make_move('a2', 'a4'))  # White moves a pawn two squares fwd
#         self.assertFalse(game.make_move('h2', 'h4'))  # White attempts to go twice in a row
#         self.assertTrue(game.make_move('b7', 'b5'))  # Black moves a pawn two squares fwd
#         self.assertTrue(game.make_move('a4', 'b5'))  # White captures a black pawn
#         self.assertTrue(game.make_move('h7', 'h5'))  # Black moves a pawn two squares fwd
#         self.assertFalse(game.make_move('a1', 'b1'))  # White attempts to move a rook to an occupied square
#         self.assertFalse(game.make_move('a1', 'c3'))  # White attempts to move a rook diagonally
#         self.assertTrue(game.make_move('a1', 'a7'))  # White captures a black pawn with a rook
#         self.assertFalse(game.make_move('h8', 'h4'))  # Black attempts to jump over another piece with a rook
#         self.assertFalse(game.make_move('h8', 'h5'))  # Black attempts to move a rook to an occupied square
#         self.assertTrue(game.make_move('a8', 'a7'))  # Black captures a white rook
#         self.assertFalse(game.make_move('h1', 'h4'))  # White attempts to jump over another piece with a rook
#         self.assertTrue(game.make_move('e2', 'e3'))  # White moves a pawn two squares fwd
#         self.assertTrue(game.make_move('a7', 'a4'))  # Black moves a rook
#         self.assertTrue(game.make_move('h2', 'h4'))  # White moves a pawn two squares fwd
#         self.assertTrue(game.make_move('a4', 'h4'))  # Black captures a white pawn
#         self.assertTrue(game.make_move('h1', 'h4'))  # White captures a black rook
#         self.assertFalse(game.make_move('h8', 'f6'))  # Black attempts to move a rook diagonally
#         self.assertTrue(game.make_move('h8', 'h6'))  # Black moves a rook
#         self.assertTrue(game.make_move('h4', 'e4'))  # White moves a rook
#         self.assertFalse(game.make_move('h6', 'e3'))  # Black attempts to capture a white pawn by moving diagonally
#         self.assertTrue(game.make_move('h6', 'e6'))  # Black moves a rook
#         self.assertTrue(game.make_move('e4', 'e6'))  # White moves a rook
#         self.assertTrue(game.make_move('h5', 'h4'))  # Black moves a pawn one square fwd
#         self.assertTrue(game.make_move('e6', 'e7'))  # White captures a black pawn
#         self.assertTrue(game.make_move('h4', 'h3'))  # Black moves a pawn one square fwd
#         self.assertTrue(game.make_move('e7', 'e8'))  # White captures black's king
#         self.assertFalse(game.make_move('h3', 'h2'))  # Black attempts to make a move after white already won
#         self.assertEqual(game.get_game_state(), 'WHITE_WON')  # Test correct game state
#
#     def test_queen_movement(self):
#         """Test queen movement."""
#         game = ChessVar()
#         self.assertFalse(game.make_move('d1', 'd3'))  # White attempts to make their queen jump over another piece
#         self.assertTrue(game.make_move('d2', 'd4'))  # White moves a pawn two squares fwd
#         self.assertFalse(game.make_move('d8', 'd6'))  # Black attempts to make their queen jump over another piece
#         self.assertTrue(game.make_move('d7', 'd5'))  # Black moves a pawn two squares fwd
#         self.assertTrue(game.make_move('d1', 'd3'))  # White moves their queen
#         self.assertTrue(game.make_move('d8', 'd6'))  # Black moves their queen
#         self.assertFalse(game.make_move('d3', 'g4'))  # White attempts to move their queen to an illegal square
#         self.assertFalse(game.make_move('d3', 'e2'))  # White attempts to move their queen to an occupied square
#         self.assertTrue(game.make_move('d3', 'h3'))  # White moves their queen
#         self.assertFalse(game.make_move('d6', 'c3'))  # Black attempts to move their queen to an illegal square
#         self.assertFalse(game.make_move('d6', 'd5'))  # Black attempts to move their queen to an occupied square
#         self.assertTrue(game.make_move('d6', 'b4'))  # Black moves their queen diagonally
#         self.assertTrue(game.make_move('h3', 'c8'))  # White captures a black bishop
#         self.assertTrue(game.make_move('b4', 'e1'))  # Black captures white's king
#         self.assertFalse(game.make_move('g2', 'g4'))  # White attempts to make a move after black already won
#         self.assertEqual(game.get_game_state(), 'BLACK_WON')  # Test correct game state
#
#     def test_king_movement(self):
#         """Test king movement."""
#         game = ChessVar()
#         self.assertTrue(game.make_move('e2', 'e4'))  # White moves a pawn two squares fwd
#         self.assertTrue(game.make_move('e7', 'e5'))  # Black moves a pawn two squares fwd
#         self.assertFalse(game.make_move('e1', 'e3'))  # White attempts to move their king more than one square fwd
#         self.assertFalse(game.make_move('e1', 'f1'))  # White attempts to move their king to an occupied square
#         self.assertTrue(game.make_move('e1', 'e2'))  # White moves their king
#         self.assertFalse(game.make_move('e8', 'f7'))  # Black attempts to move their king to an occupied square
#         self.assertFalse(game.make_move('e8', 'e6'))  # Black attempts to move their king more than one square fwd
#         self.assertTrue(game.make_move('e8', 'e7'))  # Black moves their king
#         self.assertFalse(game.make_move('e2', 'g4'))  # White attempts to move their king to an illegal square
#         self.assertTrue(game.make_move('e2', 'd3'))  # White moves their king diagonally
#         self.assertTrue(game.make_move('e7', 'f6'))  # Black moves their king diagonally
#         self.assertTrue(game.make_move('d3', 'd4'))  # White moves their king fwd
#         self.assertTrue(game.make_move('f6', 'f5'))  # Black moves their king fwd
#         self.assertTrue(game.make_move('d4', 'e5'))  # White captures a black pawn
#         self.assertTrue(game.make_move('f5', 'e4'))  # Black captures a white pawn
#         self.assertFalse(game.make_move('e5', 'e7'))  # White attempts to move their king two squares fwd
#         self.assertTrue(game.make_move('e5', 'e4'))  # White captures black's king
#         self.assertFalse(game.make_move('d8', 'e7'))  # Black attempts to make a move after white already won
#         self.assertEqual(game.get_game_state(), 'WHITE_WON')  # Test correct game state
#
#     def test_fairy_pieces(self):
#         """Test entering fairy pieces and fairy piece movement."""
#         game = ChessVar()
#         self.assertTrue(game.make_move('d2', 'd4'))  # White moves a pawn two squares fwd
#         self.assertTrue(game.make_move('g8', 'f6'))  # Black moves a knight
#         self.assertTrue(game.make_move('c1', 'f4'))  # White moves a bishop
#         self.assertTrue(game.make_move('e7', 'e6'))  # Black moves a pawn one square fwd
#         self.assertTrue(game.make_move('f4', 'c7'))  # White captures a black pawn
#         self.assertFalse(game.enter_fairy_piece('f', 'g8'))  # Black attempts to enter their falcon fairy piece
#         self.assertTrue(game.make_move('f6', 'g4'))  # Black moves a knight
#         self.assertTrue(game.make_move('c7', 'b8'))  # White captures a black knight
#         self.assertFalse(game.enter_fairy_piece('F', 'g8'))  # Black attempts to enter the white falcon fairy piece
#         self.assertFalse(game.enter_fairy_piece('f', 'f8'))  # Black attempts to enter their falcon fairy piece on an occupied square
#         self.assertFalse(game.enter_fairy_piece('f', 'a6'))  # Black attempts to enter their falcon fairy piece outside their home ranks
#         self.assertTrue(game.enter_fairy_piece('f', 'g8'))  # Black enters their falcon fairy piece
#         self.assertFalse(game.enter_fairy_piece('F', 'c1'))  # White attempts to enter their fairy piece
#         self.assertTrue(game.make_move('b1', 'c3'))  # White moves a knight
#         self.assertTrue(game.make_move('a8', 'b8'))  # Black captures a white bishop
#         self.assertFalse(game.enter_fairy_piece('f', 'd2'))  # White attempts to enter the black falcon fairy piece
#         self.assertFalse(game.enter_fairy_piece('F', 'g2'))  # White attempts to enter their falcon fairy piece on an occupied square
#         self.assertFalse(game.enter_fairy_piece('F','a3'))  # White attempts to enter their falcon fairy piece outside their home ranks
#         self.assertTrue(game.enter_fairy_piece('F', 'd2'))  # White enters their falcon fairy piece
#         self.assertFalse(game.make_move('d2', 'f4'))  # White attempts to take another turn
#         self.assertFalse(game.make_move('g8', 'g5'))  # Black attempts to make their falcon move straight forward
#         self.assertFalse(game.make_move('g8', 'e6'))  # Black attempts to make their falcon jump over another piece
#         self.assertFalse(game.enter_fairy_piece('h', 'a8'))  # Black attempts to enter a second fairy piece
#         self.assertTrue(game.make_move('f7', 'f5'))  # Black moves a pawn two squares fwd
#         self.assertFalse(game.make_move('d2', 'd3'))  # White attempts to make their falcon move straight forward
#         self.assertFalse(game.make_move('d2', 'c1'))  # White attempts to make their falcon move diagonally backwards
#         self.assertFalse(game.make_move('d2', 'b4'))  # White attempts to make their falcon jump over another piece
#         self.assertTrue(game.make_move('d2', 'h6'))  # White moves their falcon
#         self.assertTrue(game.make_move('g7', 'h6'))  # Black captures white's falcon
#         self.assertFalse(game.enter_fairy_piece('H', 'c1'))  # White attempts to enter a second fairy piece
#         self.assertTrue(game.make_move('d1', 'd3'))  # White moves their queen
#         self.assertTrue(game.make_move('f8', 'c5'))  # Black moves their bishop
#         self.assertTrue(game.make_move('d4', 'c5'))  # White captures a black bishop
#         self.assertFalse(game.enter_fairy_piece('H', 'c7'))  # Black attempts to enter the white hunter fairy piece
#         self.assertFalse(game.enter_fairy_piece('f', 'c7'))  # Black attempts to enter a second falcon fairy piece
#         self.assertFalse(game.enter_fairy_piece('h', 'a7'))  # Black attempts to enter their hunter fairy piece on an occupied square
#         self.assertFalse(game.enter_fairy_piece('h', 'c6'))  # Black attempts to enter their hunter fairy piece outside their home ranks
#         self.assertTrue(game.enter_fairy_piece('h', 'f7'))  # Black enters their hunter fairy piece
#         self.assertFalse(game.make_move('f7', 'f6'))  # Black attempts to take another turn
#         self.assertTrue(game.make_move('d3', 'f5'))  # White captures a black pawn
#         self.assertTrue(game.make_move('e6', 'f5'))  # Black captures white's queen
#         self.assertFalse(game.enter_fairy_piece('h', 'd2'))  # White attempts to enter the black hunter fairy piece
#         self.assertFalse(game.enter_fairy_piece('F', 'd2'))  # White attempts to enter a second falcon fairy piece
#         self.assertFalse(game.enter_fairy_piece('H', 'e1'))  # White attempts to enter their hunter fairy piece on an occupied square
#         self.assertFalse(game.enter_fairy_piece('H','g3'))  # White attempts to enter their hunter fairy piece outside their home ranks
#         self.assertTrue(game.enter_fairy_piece('H', 'd2'))  # White enters their hunter fairy piece
#         self.assertFalse(game.enter_fairy_piece('h', 'c7'))  # Black attempts to enter another hunter fairy piece
#         self.assertFalse(game.make_move('f7', 'd5'))  # Black attempts to move their hunter fairy piece diagonally forward
#         self.assertFalse(game.make_move('f7', 'g6'))  # Black attempts to move their hunter fairy piece diagonally forward
#         self.assertFalse(game.make_move('f7', 'f8'))  # Black attempts to move their hunter fairy piece straight backwards
#         self.assertTrue(game.make_move('f7', 'f6'))  # Black moves their hunter fairy piece
#         self.assertFalse(game.enter_fairy_piece('H', 'd1'))  # White attempts to enter another hunter fairy piece
#         self.assertFalse(game.make_move('d2', 'e3'))  # White attempts to move their hunter fairy piece diagonally forward
#         self.assertFalse(game.make_move('d2', 'd1'))  # White attempts to move their hunter fairy piece straight backwards
#         self.assertTrue(game.make_move('d2', 'd7'))  # White moves their hunter fairy piece and captures a black pawn
#         self.assertFalse(game.make_move('f6', 'c6'))  # Black attempts to move their hunter fairy piece sideways
#         self.assertFalse(game.make_move('g8', 'f8'))  # Black attempts to move their falcon fairy piece sideways
#         self.assertTrue(game.make_move('g8', 'b3'))  # Black moves their falcon
#         self.assertTrue(game.make_move('c3', 'b5'))  # White moves a knight
#         self.assertTrue(game.make_move('b3', 'b5'))  # Black captures a white knight
#         self.assertTrue(game.make_move('d7', 'd8'))  # White captures black's queen
#         self.assertTrue(game.make_move('e8', 'd8'))  # Black captures white's hunter
