# This file includes classes used for the chess game implementation:
# Parent class ChessPiece and its child classes Pawn, Knight, Bishop, Rook,
# Queen, King, Falcon, and Hunter
# Board, Player, and Chess classes

from abc import ABC, abstractmethod
from collections.abc import Collection
from enum import Enum
from typing import Optional

import numpy as np


class InvalidColorError(Exception):
    """User-defined exception for invalid chess piece color."""
    pass


class Color(Enum):
    """Enumeration representing valid chess piece colors."""
    BLACK = 1
    WHITE = 2


class ChessPiece(ABC):
    """
    Represents a chess piece with a color and label.
    Responsible for keeping track of a chess piece's team color (black or white) and its label (to distinguish the
    type of chess piece).
    Has various child classes for each type of chess piece.
    """
    def __init__(self, color: Color, label: str) -> None:
        """
        Creates a new ChessPiece object with the specified color and label.
        :param color: piece color as a Color enumeration member
        :param label: piece label as a lowercase character
        """
        self._color = color

        # If the piece is white, we change the label to an uppercase char
        if color == Color.WHITE:
            self._label = label.upper()
        else:
            self._label = label

    def get_color(self) -> Color:
        """
        Returns the chess piece's color.
        :return: piece color as a Color enumeration member
        """
        return self._color

    def get_label(self) -> str:
        """
        Returns the chess piece's label.
        :return: Label as a char
        """
        return self._label

    def get_first_move(self) -> bool:
        """
        Returns the piece's first_move value, specifying whether it is the piece's first move.
        Overridden in child classes that have this data member.
        :return:    Boolean:
                    True if it is the piece's first move
                    False otherwise
        """
        pass

    def negate_first_move_flag(self):
        """
        Negates the value of _first_move. Overridden in child classes with this member.
        :return: No return value, the data member is changed in place.
        """
        pass

    @abstractmethod
    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the piece's moveset and current state of the game board.
        Overridden in child classes.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        pass


class Pawn(ChessPiece):
    """
    Represents a pawn chess piece with a color and label.
    Responsible for ensuring that a pawn can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    Communicates with the Board class to check for opposing chess pieces in diagonal forward directions.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new Pawn object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'p')
        self._first_move = True  # Whether this is the pawn's first move

    def get_first_move(self) -> bool:
        """
        Returns the pawn's first_move value, specifying whether it is the pawn's first move.
        :return:    Boolean:
                    True if it is the pawn's first move
                    False otherwise
        """
        return self._first_move

    def negate_first_move_flag(self):
        """
        Negates the value of the _first_move private member.
        :return: No return value, the data member is changed in place.
        """
        self._first_move = not self._first_move

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the pawn's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # Check movement on first turn
        if self._first_move:
            # Don't allow moving forward more than 2 spaces
            if abs(goal_square[0] - start_square[0]) > 2:
                print("Pawns cannot move more than 2 spaces forward on their first turn!\n")
                return False

            # Don't allow jumping over another piece
            if goal_square[1] == start_square[1] and straight_move_requires_jump(start_square, goal_square, board):
                print("Pawns cannot jump over other pieces.\n")
                return False

        # Don't allow moving backwards or sideways
        if ((self._color == Color.WHITE and goal_square[0] > start_square[0])
                or (self._color == Color.BLACK and goal_square[0] < start_square[0])):
            print("Pawns cannot move backwards!\n")
            return False

        if goal_square[0] == start_square[0]:
            print("Pawns cannot move sideways!\n")
            return False

        # Check forward movement after the first turn
        if not self._first_move and goal_square[1] == start_square[1] and abs(goal_square[0] - start_square[0]) > 1:
            print("Pawns cannot move more than 1 space forward after their first turn!\n")
            return False

        # Get object on goal square to check if diagonal moves are allowed
        piece_on_goal_square = board.get_current_piece_on_square(goal_square)

        # Don't allow moving straight forward onto a square with another piece
        if start_square[1] == goal_square[1] and piece_on_goal_square:
            print("Pawns cannot capture by moving straight forward.\n")
            return False

        # Don't allow diagonal movement to columns more than 1 square away
        if abs(start_square[1] - goal_square[1]) > 1:
            print("Pawns cannot move more than one square diagonally.\n")
            return False

        # Don't allow diagonal movement to empty squares
        if abs(start_square[1] - goal_square[1]) == 1 and not piece_on_goal_square:
            print("Pawns cannot move diagonally to an empty square.\n")
            return False

        # If we get to this point, the proposed move is legal
        return True


class Knight(ChessPiece):
    """
    Represents a knight chess piece with a color and label.
    Responsible for ensuring that a knight can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new Knight object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'k')

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the knight's moveset.
        Knights are allowed to jump over other pieces.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # Can move one square left or right and two squares up or down
        if abs(goal_square[1] - start_square[1]) == 1 and abs(goal_square[0] - start_square[0]) == 2:
            return True

        # Can move two squares left or right and one square up or down
        if abs(goal_square[1] - start_square[1]) == 2 and abs(goal_square[0] - start_square[0]) == 1:
            return True

        # Otherwise, the move is not legal
        print("The knight can only move in a 2+1 or 1+2 L shape!\n")
        return False


class Bishop(ChessPiece):
    """
    Represents a bishop chess piece with a color and label.
    Responsible for ensuring that a bishop can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new Bishop object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'b')

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the bishop's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # We must check that we move the same number horizontally as vertically to reach goal square
        if abs(goal_square[1] - start_square[1]) != abs(goal_square[0] - start_square[0]):
            print("Bishops can only move diagonally!\n")
            return False

        # If the proposed move requires a jump, the move is illegal
        if diagonal_move_requires_jump(start_square, goal_square, board):
            print("Bishops cannot jump over other pieces!\n")
            return False

        # Otherwise, no jumps are required and the proposed move is legal
        return True


class Rook(ChessPiece):
    """
    Represents a rook chess piece with a color and label.
    Responsible for ensuring that a rook can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new Rook object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'r')

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the rook's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # Is goal_square on the same column or row as start_square?
        if goal_square[1] != start_square[1] and goal_square[0] != start_square[0]:
            print("Rooks can only move horizontally or vertically!\n")
            return False

        # If the proposed move requires a jump, the move is illegal
        if straight_move_requires_jump(start_square, goal_square, board):
            print("Rooks cannot jump over other pieces!\n")
            return False

        # Otherwise, no jumps are required and the proposed move is legal
        return True


class Queen(ChessPiece):
    """
    Represents a queen chess piece with a color and label.
    Responsible for ensuring that a queen can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new Queen object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'q')

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the queen's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # We must check that we move either diagonally or straight up/down/left/right
        if ((abs(goal_square[1] - start_square[1]) != abs(goal_square[0] - start_square[0])) and
                goal_square[1] != start_square[1] and goal_square[0] != start_square[0]):
            print("A queen can only move diagonally, or straight up, down, left or right!\n")
            return False

        # If a proposed diagonal move requires a jump, the move is illegal
        if diagonal_move_requires_jump(start_square, goal_square, board):
            print("A queen cannot jump over other pieces!\n")
            return False

        # If a proposed straight move requires a jump, the move is illegal
        if ((goal_square[1] == start_square[1] or goal_square[0] == start_square[0]) and
                straight_move_requires_jump(start_square, goal_square, board)):
            print("A queen cannot jump over other pieces!\n")
            return False

        # Otherwise, no jumps are required and the proposed move is legal
        return True


class King(ChessPiece):
    """
    Represents a king chess piece with a color and label.
    Responsible for ensuring that a king can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new King object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'g')

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the king's moveset.
        Since a king can only move one space in each direction, we do not have to check for jumps.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # Move is illegal if goal square is more than one square away from start square
        if abs(goal_square[1] - start_square[1]) > 1 or abs(goal_square[0] - start_square[0]) > 1:
            print("A king can only move one square in any direction!\n")
            return False

        # Otherwise, the proposed move is legal
        return True


class Falcon(ChessPiece):
    """
    Represents a falcon chess piece with a color and label.
    Responsible for ensuring that a falcon can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new Falcon object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'f')

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the falcon's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # Falcon's cannot move straight left or right
        if start_square[0] == goal_square[0]:
            print("Falcons cannot move straight left or right!\n")
            return False

        # Checks for white pieces
        if self._color == Color.WHITE:
            # If we are trying to move backwards, but not within the same column, the move is illegal
            if goal_square[0] > start_square[0] and goal_square[1] != start_square[1]:
                print("Falcons can only move straight backwards!\n")
                return False

            # If we are trying to move forward, but not on a diagonal, the move is illegal
            if (goal_square[0] < start_square[0] and
                    abs(goal_square[1] - start_square[1]) != abs(goal_square[0] - start_square[0])):
                print("Falcons can only move diagonally forward!\n")
                return False

            # If we are trying to move backwards, we must check for jumps in that direction
            if goal_square[0] > start_square[0]:
                # If a proposed straight move requires a jump, the move is illegal
                if straight_move_requires_jump(start_square, goal_square, board):
                    print("A falcon cannot jump over other pieces!\n")
                    return False

                # Otherwise, no jumps are required and the proposed move is legal
                return True

            # If we are trying to move diagonally, we must check for jumps in that direction
            # If a proposed diagonal move requires a jump, the move is illegal
            if diagonal_move_requires_jump(start_square, goal_square, board):
                print("A falcon cannot jump over other pieces!\n")
                return False

            # Otherwise, no jumps are required and the proposed move is legal
            return True

        # Checks for black pieces
        if self._color == Color.BLACK:
            # If we are trying to move backwards, but not within the same column, the move is illegal
            if goal_square[0] < start_square[0] and goal_square[1] != start_square[1]:
                print("Falcons can only move straight backwards!\n")
                return False

            # If we are trying to move forward, but not on a diagonal, the move is illegal
            if (goal_square[0] > start_square[0] and
                    abs(goal_square[1] - start_square[1]) != abs(goal_square[0] - start_square[0])):
                print("Falcons can only move diagonally forward!\n")
                return False

            # If we are trying to move backwards, we must check for jumps in that direction
            if goal_square[0] < start_square[0]:
                # If a proposed straight move requires a jump, the move is illegal
                if straight_move_requires_jump(start_square, goal_square, board):
                    print("A falcon cannot jump over other pieces!\n")
                    return False

                # Otherwise, no jumps are required and the proposed move is legal
                return True

            # If we are trying to move diagonally, we must check for jumps in that direction
            if goal_square[0] > start_square[0]:
                # If a proposed diagonal move requires a jump, the move is illegal
                if diagonal_move_requires_jump(start_square, goal_square, board):
                    print("A falcon cannot jump over other pieces!\n")
                    return False

                # Otherwise, no jumps are required and the proposed move is legal
                return True

        # If we get to this point, the chess piece color is invalid
        raise InvalidColorError("This is not a valid chess piece color.")


class Hunter(ChessPiece):
    """
    Represents a hunter chess piece with a color and label.
    Responsible for ensuring that a hunter can only attempt movements defined within its moveset.
    Not responsible for checking other movement conditions. These checks are done by Chess instead.
    Inherits from ChessPiece.
    """
    def __init__(self, color: Color) -> None:
        """
        Creates a new Hunter object with the specified color and label.
        :param color: piece color as a Color enumeration member
        """
        super().__init__(color, 'h')

    def move_legal(self, start_square: np.array, goal_square: np.array, board: "Board") -> bool:
        """
        Check if a proposed move is legal according to the hunter's moveset and current state of the game board.
        This method also verifies if any other pieces are in the way of the proposed move.
        :param start_square: the start position as a vector [row, column]
        :param goal_square: the goal position as a vector [row, column]
        :param board: the game's board as a Board object
        :return:    Boolean:
                    False if move is illegal
                    True if move is legal
        """
        # Hunter's cannot move straight left or right
        if start_square[0] == goal_square[0]:
            print("Hunters cannot move straight left or right!\n")
            return False

        # Checks for white pieces
        if self._color == Color.WHITE:
            # If we are trying to move forward, but not within the same column, the move is illegal
            if goal_square[0] < start_square[0] and goal_square[1] != start_square[1]:
                print("Hunters can only move straight forward!\n")
                return False

            # If we are trying to move backward, but not on a diagonal, the move is illegal
            if (goal_square[0] > start_square[0] and
                    abs(goal_square[1] - start_square[1]) != abs(goal_square[0] - start_square[0])):
                print("Hunters can only move diagonally backward!\n")
                return False

            # If we are trying to move forward, we must check for jumps in that direction
            if goal_square[0] < start_square[0]:
                # If a proposed straight move requires a jump, the move is illegal
                if straight_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False

                # Otherwise, no jumps are required and the proposed move is legal
                return True

            # If we are trying to move backward, we must check for jumps in that direction
            if goal_square[0] > start_square[0]:
                # If a proposed diagonal move requires a jump, the move is illegal
                if diagonal_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False

                # Otherwise, no jumps are required and the proposed move is legal
                return True

        # Checks for black pieces
        if self._color == Color.BLACK:
            # If we are trying to move forward, but not within the same column, the move is illegal
            if goal_square[0] > start_square[0] and goal_square[1] != start_square[1]:
                print("Hunters can only move straight forward!\n")
                return False

            # If we are trying to move backward, but not on a diagonal, the move is illegal
            if (goal_square[0] < start_square[0] and
                    abs(goal_square[1] - start_square[1]) != abs(goal_square[0] - start_square[0])):
                print("Hunters can only move diagonally backward!\n")
                return False

            # If we are trying to move forward, we must check for jumps in that direction
            if goal_square[0] > start_square[0]:
                # If a proposed straight move requires a jump, the move is illegal
                if straight_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False

                # Otherwise, no jumps are required and the proposed move is legal
                return True

            # If we are trying to move backward, we must check for jumps in that direction
            if goal_square[0] < start_square[0]:
                # If a proposed diagonal move requires a jump, the move is illegal
                if diagonal_move_requires_jump(start_square, goal_square, board):
                    print("A hunter cannot jump over other pieces!\n")
                    return False

                # Otherwise, no jumps are required and the proposed move is legal
                return True

        # If we get to this point, the chess piece color is invalid
        raise InvalidColorError("This is not a valid chess piece color.")


class Board:
    """
    Represents a standard 8x8 chess board where the rows are labeled with numbers 1-8 and the columns are labeled with
    letters a-h.
    Responsible for initializing and storing the current layout of the chess board, printing out a visualization of the
    current board layout, and completing a move by updating the two relevant squares on the board after a move has been
    validated by the Chess class.
    Needs to communicate with the ChessPiece class (and its various child classes) since these pieces can be present on
    the board. Also communicates with the Chess class to update its layout when needed.
    """
    # Explicitly specify expected types for the Board layout
    _layout: list[list[ChessPiece | None]]

    def __init__(self) -> None:
        """
        Creates a new Board object.
        The chess board is represented by a list of lists.
        Each sublist represents a row of the Board, containing ChessPiece objects.
        The first sublist corresponds to row label 8 on the chess board.
        The last sublist corresponds to row label 1 on the chess board.
        The elements of each sublist represent columns labeled a - h on the chess board.
        If a square on the board is empty, its value is None.
        """
        b = Color.BLACK
        w = Color.WHITE
        self._layout = [
            [Rook(b), Knight(b), Bishop(b), Queen(b), King(b), Bishop(b), Knight(b), Rook(b)],
            [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w)],
            [Rook(w), Knight(w), Bishop(w), Queen(w), King(w), Bishop(w), Knight(w), Rook(w)]
        ]

        self._width = 8
        self._height = 8
        self._start_ord = ord('a')

    def get_width(self) -> int:
        """
        Get the board's width.
        :return: Board object's width as an integer
        """
        return self._width

    def get_height(self) -> int:
        """
        Get the board's height.
        :return: Board object's height as an integer
        """
        return self._height

    def get_current_piece_on_square(self, square: np.array) -> Optional[ChessPiece]:
        """
        Get the current chess piece on the specified square.
        :param square: square as a vector [row, column]
        :return: ChessPiece object currently located on square, None if the square is empty
        """
        return self._layout[square[0]][square[1]]

    def print(self) -> None:
        """
        Prints out the current layout of the board.
        :return: No return value
        """
        # Print column labels at the top
        print('  ', end='')
        for val in range(self._start_ord, self._start_ord + self._width):
            print(f" {chr(val)} ", end='')
        print('\n')

        curr_row = self._height
        for row in self._layout:
            print(f"{curr_row} ", end='')
            for piece in row:
                # If there is no piece on the square, print an underscore character
                if not piece:
                    print(' _ ', end='')
                # If there is a piece, print its label
                else:
                    print(f" {piece.get_label()} ", end='')
            # Move to next line
            print('\n')
            curr_row -= 1

        # Print column labels at the bottom
        print('  ', end='')
        for val in range(self._start_ord, self._start_ord + self._width):
            print(f" {chr(val)} ", end='')
        print('\n\n')

    def update_move(self, start_square: np.array, goal_square: np.array, piece: ChessPiece) -> None:
        """
        Update the current state of the board by updating start_square to None (the piece was moved away from this
        square) and goal_square to the specified piece (the piece was moved here).
        :param start_square: first square as a vector [row, column]
        :param goal_square: second square as a vector [row, column]
        :param piece: ChessPiece object to be placed on goal_square
        :return: No return value, the board layout is updated in place
        """
        self._layout[start_square[0]][start_square[1]] = None

        self._layout[goal_square[0]][goal_square[1]] = piece

    def update_piece_entered(self, square: np.array, piece: ChessPiece) -> None:
        """
        Update the current state of the board by entering the specified piece on the specified square.
        :param square: square as a vector [row, column]
        :param piece: ChessPiece object to be placed on the specified square
        :return: No return value, the layout is updated in place
        """
        self._layout[square[0]][square[1]] = piece


def traveling_on_axis_requires_jump(start_square: np.array, goal_square: np.array, board: Board,
                                    axis: np.array) -> bool:
    """
    Checks whether other pieces are in the way when moving from the specified start square to the specified goal square
    along the specified axis (if a move along the axis requires a jump).
    :param start_square: the start position as a vector [row, column]
    :param goal_square: the goal position as a vector [row, column]
    :param board: the game's board as a Board object
    :param axis: directional axis as a unit vector [x direction, y direction]
    :return:    Boolean:
                True if the move requires a jump
                False if move doesn't require a jump
    """
    current_square = start_square + axis
    while 0 < current_square[0] < board.get_height() or 0 < current_square[1] < board.get_width():
        # If we reach the goal square, the move did not require any jumps
        if current_square[0] == goal_square[0] and current_square[1] == goal_square[1]:
            return False

        # If we encounter another piece, the move requires a jump
        current_square_tuple = int(current_square[0]), int(current_square[1])
        if board.get_current_piece_on_square(current_square_tuple):
            return True

        current_square += axis


def diagonal_move_requires_jump(start_square: np.array, goal_square: np.array, board: Board) -> bool:
    """
    Checks whether other pieces are in the way of a proposed diagonal move (if a move requires a jump).
    :param start_square: the start position as a vector [row, column]
    :param goal_square: the goal position as a vector [row, column]
    :param board: the game's board as a Board object
    :return:    Boolean:
                True if the move requires a jump
                False if move doesn't require a jump
    """
    # Bottom right direction
    if goal_square[0] > start_square[0] and goal_square[1] > start_square[1]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([1, 1]))

    # Top right direction
    if goal_square[0] < start_square[0] and goal_square[1] > start_square[1]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([-1, 1]))

    # Bottom left direction
    if goal_square[0] > start_square[0] and goal_square[1] < start_square[1]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([1, -1]))

    # Top left direction
    if goal_square[0] < start_square[0] and goal_square[1] < start_square[1]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([-1, -1]))


def straight_move_requires_jump(start_square: np.array, goal_square: np.array, board: Board) -> bool:
    """
    Checks whether other pieces are in the way of a proposed up/down or left/right move (if a move requires a jump).
    :param start_square: the start position as a vector [row, column]
    :param goal_square: the goal position as a vector [row, column]
    :param board: the game's board as a Board object
    :return:    Boolean:
                True if the move requires a jump
                False if move doesn't require a jump
    """
    # Down direction
    if goal_square[0] > start_square[0]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([1, 0]))

    # Up direction
    if goal_square[0] < start_square[0]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([-1, 0]))

    # Left direction
    if goal_square[1] < start_square[1]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([0, -1]))

    # Right direction
    if goal_square[1] > start_square[1]:
        return traveling_on_axis_requires_jump(start_square, goal_square, board, np.array([0, 1]))


class Player:
    """
    Represents a chess player.
    Responsible for keeping track of the player's team color (black or white), available fairy pieces, and previously
    captured pieces (to check if the player is allowed to enter a fairy piece).
    Communicates with ChessPiece class and its various child classes to keep track of fairy pieces and captured
    pieces.
    """
    # Explicitly specify expected types for the fairy pieces list
    _fairy_pieces: list[ChessPiece]

    def __init__(self, color: Color) -> None:
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

    def get_fairy_pieces(self) -> Collection[ChessPiece]:
        """
        Returns the player's current list of available fairy pieces that can be entered into the game.
        :return: Python list of ChessPiece objects
        """
        return self._fairy_pieces

    def get_captured_pieces(self) -> Collection[ChessPiece]:
        """
        Returns a list of the pieces the player has lost in the game so far.
        :return: Python list of ChessPiece objects
        """
        return self._captured_pieces

    def add_captured_piece(self, captured_piece: ChessPiece) -> None:
        """
        Adds the specified captured piece to the list of captured pieces for this player.
        :param captured_piece: the captured piece as a ChessPiece object
        :return: No return value, the list is changed in place
        """
        self._captured_pieces.append(captured_piece)

    def remove_fairy_piece(self, fairy_piece: ChessPiece) -> None:
        """
        Remove the specified fairy piece from the player's list of available fairy pieces.
        :param fairy_piece: the entered fairy piece as a ChessPiece object
        :return: No return value, the list is changed in place
        """
        self._fairy_pieces.remove(fairy_piece)

    def print_fairy_pieces(self) -> None:
        """
        Prints out a list of the player's available fairy pieces.
        :return: No return value
        """
        for fairy_piece in self._fairy_pieces:
            print(fairy_piece)

    def print_captured_pieces(self) -> None:
        """
        Prints out a list of the player's pieces that have been captured by the other player on previous turns.
        :return: No return value
        """
        for captured_piece in self._captured_pieces:
            print(captured_piece)


class Chess:
    """
    Represents a falcon-hunter chess game.
    Responsible for the overall game loop: initializes a chess board, initializes two players, sets which player's
    turn it is, and keeps track of the game state (whether the game is ongoing or which player won).
    This class is also responsible for making a move and ensuring that the move is legal, as well as entering a fairy
    piece to the game if it's allowed.
    Communicates with the Board class to initialize and update the chess board, with the Player class to create and keep
    track of the two players, and the ChessPiece class (and its various child classes) to verify if moves are legal
    according to a piece's moveset.
    """
    def __init__(self) -> None:
        """
        Creates a new chess game object.
        """
        # Initialize the board.
        self._board = Board()

        # Initialize the two players.
        self._white = Player(Color.WHITE)
        self._black = Player(Color.BLACK)

        # White begins per the standard rules
        # Integer 1: White's turn, Integer -1: Black's turn
        # This way, to switch turns, all we have to do is multiply by (-1) to flip the value
        self._player_turn = 1
        # TODO: Count all turns, use mod to determine current turn.

        # Initial game state
        # Other possible states are 'WHITE_WON' and 'BLACK_WON'
        self._game_state = "UNFINISHED"
        # TODO: Replace game_state with an enum.

    def print_board(self) -> None:
        """
        Prints out the current state of the chess board.
        :return: No return value, prints out the board.
        """
        self._board.print()

    def get_game_state(self) -> str:
        """
        Returns the game's current state.
        :return: game state as a string
        """
        return self._game_state

    def get_player_turn(self) -> int:
        """
        Returns the value representing which player's turn it is.
        :return: player turn as an integer, 1 if it's White's turn, -1 if it's Black's turn
        """
        return self._player_turn

    def go_to_next_turn(self) -> None:
        """
        Changes the current turn to the other player.
        A value of 1 corresponds to player1 and a value of -1 corresponds to player2.
        :return: No return value, changes self._player_turn in place
        """
        self._player_turn *= (-1)

    def parse_square(self, square: str) -> np.array:
        """
        Converts a string of format 'ColRow' to a vector of two integers [row, col].
        :param square: square as a string of two characters representing 'ColRow' on the chess board
        :return: the specified square as a vector [row, column]
        """
        row = 8 - int(square[1])
        column = ord(square[0]) - ord('a')
        return np.array([row, column])

    def format_square(self, square: np.array) -> str:
        """
        Converts a vector of two integers representing a square on the chess board as [row, col] to a string
        of format 'ColRow'.
        :param square: the specified square as a vector [row, column]
        :return: square as a string of two characters representing 'ColRow' on the chess board
        """
        row_str = 8 - square[0]
        col_str = ord('a') + square[1]  # TODO: Make getter method Board.get_start_ord
        return str(col_str) + str(row_str)

    # TODO: Take in coordinates instead of square strings. Decouple the frontend and backend as much as possible.
    #  The UI should get data from the user and pass it to the engine in the format the engine understands, rather
    #  than the engine trying to understand all possible UI formats. The same is true in the reverse direction.
    def make_move(self, start_square: str, goal_square: str) -> bool:
        """
        Moves a piece from start_square to goal_square. Takes user entered strings as input and internally converts the
        strings to a tuple of two integers as used by the board's layout.
        This separates the user from the internal implementation.
        :param start_square: the start position as a string
        :param goal_square: the goal position as a string
        :return:    Boolean:
                    False if move is illegal or game has already been won
                    True if move is legal
        """
        # Check if move is legal:
        # Is the game over?
        if self._game_state != "UNFINISHED":
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
        if row < 1 or row > self._board.get_height():
            print("Row out of bounds! Cannot move chess piece off the board.\n")
            return False

        # Convert input strings to tuples
        start_square = self.parse_square(start_square)
        goal_square = self.parse_square(goal_square)

        piece_on_start_square = self._board.get_current_piece_on_square(start_square)
        # Does start_square contain a chess piece at all?
        if not piece_on_start_square:
            print("The specified start square does not contain a chess piece. Move cannot be completed.\n")
            return False

        # Does start_square contain a piece belonging to the current player?
        # If color is 'black' and player_turn = 1, move is illegal
        # TODO: Replace `_player_turn` check with a `get_turn_color()` method.
        piece_on_start_square_color = piece_on_start_square.get_color()
        if piece_on_start_square_color == Color.BLACK and self._player_turn == 1:
            print("It's white's turn! Cannot move a black chess piece.\n")
            return False

        # If color is 'white' and player_turn = -1, move is illegal
        if piece_on_start_square_color == Color.WHITE and self._player_turn == -1:
            print("It's black's turn! Cannot move a white chess piece.\n")
            return False

        # Is the proposed move legal for this type of ChessPiece?
        if not piece_on_start_square.move_legal(start_square, goal_square, self._board):
            return False

        # Does goal_square contain a piece from the current player?
        piece_on_goal_square = self._board.get_current_piece_on_square(goal_square)

        if piece_on_goal_square:
            piece_on_goal_square_color = piece_on_goal_square.get_color()
            # If color is 'white' and player_turn = 1, move is illegal
            if piece_on_goal_square_color == Color.WHITE and self._player_turn == 1:
                print("The goal square already contains a white chess piece!\n")
                return False

            # If color is 'black' and player_turn = -1, move is illegal
            if piece_on_goal_square_color == Color.BLACK and self._player_turn == -1:
                print("The goal square already contains a black chess piece!\n")
                return False

            # If we reach this point, the proposed move is legal!

            # Does goal_square contain a piece? Capture it!
            # Add captured piece to that players list of captured pieces
            # TODO: Collapse conditional by using a `self._players: dict[PlayerColor, Player]` structure.
            if piece_on_goal_square_color == Color.WHITE:
                self._white.add_captured_piece(piece_on_goal_square)
                print("Black captured a piece!\n")
                print("White's captured pieces: ", end=' ')
                for piece in self._white.get_captured_pieces():
                    print(piece.get_label(), end=' ')
                print('\n')
            elif piece_on_goal_square_color == Color.BLACK:
                self._black.add_captured_piece(piece_on_goal_square)
                print("White captured a piece!\n")
                print("Black's captured pieces: ", end=' ')
                for piece in self._black.get_captured_pieces():
                    print(piece.get_label(), end=' ')
                print('\n')

            # If the captured piece was a king, update the game state
            # If the black king was captured
            if piece_on_goal_square.get_label() == 'g':
                self._game_state = "WHITE_WON"
                print("White has captured Black's king! White wins the game!\n")
            # If the white king was captured
            elif piece_on_goal_square.get_label() == 'G':
                self._game_state = "BLACK_WON"
                print("Black has captured White's king! Black wins the game!\n")

        # Complete the move
        self._board.update_move(start_square, goal_square, piece_on_start_square)

        # If the moved piece was a pawn, and it was the pawn's first turn, flip
        # the first_move flag
        if piece_on_start_square.get_label().lower() == 'p' and piece_on_start_square.get_first_move():
            piece_on_start_square.negate_first_move_flag()

        # Print out the updated board and go to next turn
        self._board.print()
        self.go_to_next_turn()
        return True

    def enter_fairy_piece(self, piece_type: str, square: str) -> bool:
        """
        Enters the specified fairy piece into the game on the specified square.
        :param piece_type: fairy piece as a char
        :param square: square to place the piece on as a string label
        :return:    Boolean:
                    False if the piece is not allowed to enter this square at this turn
                    True if the piece can enter the specified square legally
        """
        square_row = int(square[1])

        # Is the game over?
        if self._game_state != "UNFINISHED":
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
        # TODO: Refactor into a `Player.count_major_pieces()` method.
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

        # Convert square label to tuple of integers
        square = self.parse_square(square)

        piece_on_square = self._board.get_current_piece_on_square(square)
        # Does the specified square contain a chess piece already?
        if piece_on_square:
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
        if not fairy_piece:
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
