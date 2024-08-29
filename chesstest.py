# Test file for chess.py

import unittest
from chess import Chess
from chess import GameState


class TestChess(unittest.TestCase):
    """Contains unit tests for the Chess class"""
    def make_move(self, game: Chess, start_square: str, goal_square: str) -> bool:
        """
        Helper function to test making moves using input strings for start and goal squares.
        :param game: the current game to be tested as a Chess object
        :param start_square: start square as a string with format 'ColRow'
        :param goal_square: goal square as a string with format 'ColRow'
        :return:    Boolean:
                    True if move was made successfully
                    False otherwise
        """
        start_square = game.parse_square(start_square)
        goal_square = game.parse_square(goal_square)

        return game.make_move(start_square, goal_square)

    def enter_fairy_piece(self, game: Chess, piece_type: str, square: str) -> bool:
        """
        Helper function to test entering a fairy piece using an input string for square.
        :param game: the current game to be tested as a Chess object
        :param piece_type: fairy piece as a char
        :param square: square as a string with format 'ColRow'
        :return:    Boolean:
                    True if the fairy piece was entered successfully
                    False otherwise
        """
        square = game.parse_square(square)

        return game.enter_fairy_piece(piece_type, square)

    def test_basic_make_move(self):
        """Test basic functionality of the make_move() method."""
        game = Chess()
        self.assertFalse(self.make_move(game,'c3', 'c4'))  # Attempt to make a move from an empty start square
        self.assertFalse(self.make_move(game,'f7', 'f5'))  # Attempt to move a piece that doesn't belong to the current player
        self.assertFalse(self.make_move(game,'g1', 'i2'))  # Attempt to move a piece to a column that isn't on the board
        self.assertFalse(self.make_move(game,'a1', 'Z1'))  # Attempt to move a piece to a column that isn't on the board
        self.assertFalse(self.make_move(game,'e1', 'e0'))  # Attempt to move a piece to a row that isn't on the board
        self.assertFalse(self.make_move(game,'g2', 'g9'))  # Attempt to move a piece to a row that isn't on the board
        self.assertFalse(self.make_move(game,'h1', 'g1'))  # Attempt to move a piece to a square that already contains a piece by the current player

    def test_pawn_movement(self):
        """Test pawn movement."""
        game = Chess()
        self.assertTrue(self.make_move(game, 'c2', 'c4'))  # White moves two squares fwd
        self.assertTrue(self.make_move(game, 'd7', 'd5'))  # Black moves two squares fwd
        self.assertTrue(self.make_move(game, 'c4', 'd5'))  # White captures the black pawn
        self.assertFalse(self.make_move(game, 'h2', 'h3'))  # White tries to make another move
        self.assertTrue(self.make_move(game, 'g7', 'g6'))  # Black moves one square fwd
        self.assertTrue(self.make_move(game, 'f2', 'f4'))  # White moves two squares fwd
        self.assertTrue(self.make_move(game, 'f7', 'f5'))  # Black moves two squares fwd
        self.assertFalse(self.make_move(game, 'f4', 'f5'))  # White tries to capture by going straight fwd
        self.assertTrue(self.make_move(game, 'e2', 'e4'))  # White moves two squares fwd
        self.assertTrue(self.make_move(game, 'f5', 'e4'))  # Black captures a white pawn
        self.assertFalse(self.make_move(game, 'f4', 'f3'))  # White tries to move a pawn backwards
        self.assertTrue(self.make_move(game, 'a2', 'a3'))  # White moves pawn one square fwd
        self.assertFalse(self.make_move(game, 'e4', 'e5'))  # Black tries to move a pawn backwards
        self.assertTrue(self.make_move(game, 'e4', 'e3'))  # Black moves pawn one square fwd
        self.assertTrue(self.make_move(game, 'b2', 'b4'))  # White moves pawn two squares fwd
        self.assertFalse(self.make_move(game, 'e3', 'f4'))  # Black tries capturing backwards
        self.assertTrue(self.make_move(game, 'g6', 'g5'))  # Black moves pawn one square fwd
        self.assertTrue(self.make_move(game, 'd5', 'd6'))  # White moves pawn one square fwd
        self.assertTrue(self.make_move(game, 'g5', 'g4'))  # Black moves pawn one square fwd
        self.assertFalse(self.make_move(game, 'd6', 'c6'))  # White tries to move pawn one square sideways
        self.assertTrue(self.make_move(game, 'd6', 'e7'))  # White captures a black pawn
        self.assertTrue(self.make_move(game, 'g4', 'g3'))  # Black moves pawn one square fwd
        self.assertTrue(self.make_move(game, 'e7', 'd8'))  # White captures black's queen
        self.assertFalse(self.make_move(game, 'c7', 'd7'))  # Black tries to move pawn one square sideways
        self.assertFalse(self.make_move(game, 'b7', 'a6'))  # Black tries to move pawn diagonally fwd onto an empty square
        self.assertTrue(self.make_move(game, 'b7', 'b6'))  # Black moves pawn one square fwd
        self.assertFalse(self.make_move(game, 'g2', 'g4'))  # White tries to jump over a black pawn
        self.assertFalse(self.make_move(game, 'a3', 'a5'))  # White tries to move pawn two squares fwd when it is not the pawn's first turn
        self.assertFalse(self.make_move(game, 'd2', 'd5'))  # White tries to move pawn more than two squares on first turn
        self.assertFalse(self.make_move(game, 'b4', 'd6'))  # White tries to move pawn more than 1 space diagonally
        self.assertTrue(self.make_move(game, 'd2', 'd3'))  # White moves pawn one square fwd
        self.assertFalse(self.make_move(game, 'b6', 'b4'))  # Black tries to move pawn two squares fwd when it is not the pawn's first turn
        self.assertFalse(self.make_move(game, 'h7', 'h4'))  # Black tries to move pawn more than two squares on first turn
        self.assertFalse(self.make_move(game, 'c7', 'e5'))  # Black tries to move pawn more than 1 space diagonally
        self.assertTrue(self.make_move(game, 'c7', 'c5'))  # Black moves pawn one square fwd

    def test_knight_movement(self):
        """Test knight movement."""
        game = Chess()
        self.assertTrue(self.make_move(game, 'b1', 'a3'))  # White moves a knight
        self.assertTrue(self.make_move(game, 'g8', 'f6'))  # Black moves a knight
        self.assertTrue(self.make_move(game, 'g1', 'f3'))  # White moves a knight
        self.assertFalse(self.make_move(game, 'b8', 'b6'))  # Black tries to move a knight illegally
        self.assertTrue(self.make_move(game, 'b8', 'a6'))  # Black moves a knight
        self.assertFalse(self.make_move(game, 'a3', 'c2'))  # White tries to move a knight onto an occupied square
        self.assertFalse(self.make_move(game, 'a3', 'd4'))  # White tries to move a knight illegally
        self.assertTrue(self.make_move(game, 'a3', 'b5'))  # White moves a knight
        self.assertTrue(self.make_move(game, 'a6', 'b4'))  # Black moves a knight and jumps over a white knight
        self.assertTrue(self.make_move(game, 'b5', 'c7'))  # White moves a knight and captures a black pawn
        self.assertTrue(self.make_move(game, 'b4', 'a2'))  # Black moves a knight and captures a white pawn
        self.assertTrue(self.make_move(game, 'c7', 'e8'))  # White moves a knight and captures the black king
        self.assertFalse(self.make_move(game, 'a2', 'c1'))  # Black attempts to make a move after white already won
        self.assertEqual(game.get_game_state(), GameState.WHITE_WON)  # Test correct game state

    def test_bishop_movement(self):
        """Test bishop movement."""
        game = Chess()
        self.assertFalse(self.make_move(game, 'd7', 'd5'))  # Black attempts to move first
        self.assertTrue(self.make_move(game, 'g2', 'g4'))  # White moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'd7', 'd5'))  # Black moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'f1', 'h3'))  # White moves a bishop
        self.assertFalse(self.make_move(game, 'c8', 'a6'))  # Black attempts to make a bishop jump over a pawn
        self.assertTrue(self.make_move(game, 'c8', 'g4'))  # Black moves a bishop and captures a white pawn
        self.assertFalse(self.make_move(game, 'h3', 'h4'))  # White tries to move a bishop straight upwards
        self.assertTrue(self.make_move(game, 'h3', 'g4'))  # White captures a black bishop
        self.assertTrue(self.make_move(game, 'e7', 'e5'))  # Black moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'g4', 'c8'))  # White moves a bishop
        self.assertTrue(self.make_move(game, 'f8', 'c5'))  # Black moves a bishop
        self.assertFalse(self.make_move(game, 'c8', 'a6'))  # White tries to move a bishop by jumping over a black pawn
        self.assertTrue(self.make_move(game, 'c8', 'e6'))  # White moves a bishop
        self.assertFalse(self.make_move(game, 'c5', 'a5'))  # Black tries to move a bishop sideways
        self.assertFalse(self.make_move(game, 'c5', 'a7'))  # Black tries to move a bishop to an occupied square
        self.assertTrue(self.make_move(game, 'c5', 'f2'))  # Black captures a white pawn
        self.assertFalse(self.make_move(game, 'e6', 'e8'))  # White tries to capture black's king with a bishop
        self.assertTrue(self.make_move(game, 'e6', 'f7'))  # White captures a black pawn
        self.assertTrue(self.make_move(game, 'f2', 'e1'))  # Black captures white's king
        self.assertFalse(self.make_move(game, 'f7', 'g8'))  # White attempts to make a move after black already won
        self.assertEqual(game.get_game_state(), GameState.BLACK_WON)  # Test correct game state

    def test_rook_movement(self):
        """Test rook movement."""
        game = Chess()
        self.assertTrue(self.make_move(game, 'a2', 'a4'))  # White moves a pawn two squares fwd
        self.assertFalse(self.make_move(game, 'h2', 'h4'))  # White attempts to go twice in a row
        self.assertTrue(self.make_move(game, 'b7', 'b5'))  # Black moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'a4', 'b5'))  # White captures a black pawn
        self.assertTrue(self.make_move(game, 'h7', 'h5'))  # Black moves a pawn two squares fwd
        self.assertFalse(self.make_move(game, 'a1', 'b1'))  # White attempts to move a rook to an occupied square
        self.assertFalse(self.make_move(game, 'a1', 'c3'))  # White attempts to move a rook diagonally
        self.assertTrue(self.make_move(game, 'a1', 'a7'))  # White captures a black pawn with a rook
        self.assertFalse(self.make_move(game, 'h8', 'h4'))  # Black attempts to jump over another piece with a rook
        self.assertFalse(self.make_move(game, 'h8', 'h5'))  # Black attempts to move a rook to an occupied square
        self.assertTrue(self.make_move(game, 'a8', 'a7'))  # Black captures a white rook
        self.assertFalse(self.make_move(game, 'h1', 'h4'))  # White attempts to jump over another piece with a rook
        self.assertTrue(self.make_move(game, 'e2', 'e3'))  # White moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'a7', 'a4'))  # Black moves a rook
        self.assertTrue(self.make_move(game, 'h2', 'h4'))  # White moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'a4', 'h4'))  # Black captures a white pawn
        self.assertTrue(self.make_move(game, 'h1', 'h4'))  # White captures a black rook
        self.assertFalse(self.make_move(game, 'h8', 'f6'))  # Black attempts to move a rook diagonally
        self.assertTrue(self.make_move(game, 'h8', 'h6'))  # Black moves a rook
        self.assertTrue(self.make_move(game, 'h4', 'e4'))  # White moves a rook
        self.assertFalse(self.make_move(game, 'h6', 'e3'))  # Black attempts to capture a white pawn by moving diagonally
        self.assertTrue(self.make_move(game, 'h6', 'e6'))  # Black moves a rook
        self.assertTrue(self.make_move(game, 'e4', 'e6'))  # White moves a rook
        self.assertTrue(self.make_move(game, 'h5', 'h4'))  # Black moves a pawn one square fwd
        self.assertTrue(self.make_move(game, 'e6', 'e7'))  # White captures a black pawn
        self.assertTrue(self.make_move(game, 'h4', 'h3'))  # Black moves a pawn one square fwd
        self.assertTrue(self.make_move(game, 'e7', 'e8'))  # White captures black's king
        self.assertFalse(self.make_move(game, 'h3', 'h2'))  # Black attempts to make a move after white already won
        self.assertEqual(game.get_game_state(), GameState.WHITE_WON)  # Test correct game state

    def test_queen_movement(self):
        """Test queen movement."""
        game = Chess()
        self.assertFalse(self.make_move(game, 'd1', 'd3'))  # White attempts to make their queen jump over another piece
        self.assertTrue(self.make_move(game, 'd2', 'd4'))  # White moves a pawn two squares fwd
        self.assertFalse(self.make_move(game, 'd8', 'd6'))  # Black attempts to make their queen jump over another piece
        self.assertTrue(self.make_move(game, 'd7', 'd5'))  # Black moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'd1', 'd3'))  # White moves their queen
        self.assertTrue(self.make_move(game, 'd8', 'd6'))  # Black moves their queen
        self.assertFalse(self.make_move(game, 'd3', 'g4'))  # White attempts to move their queen to an illegal square
        self.assertFalse(self.make_move(game, 'd3', 'e2'))  # White attempts to move their queen to an occupied square
        self.assertTrue(self.make_move(game, 'd3', 'h3'))  # White moves their queen
        self.assertFalse(self.make_move(game, 'd6', 'c3'))  # Black attempts to move their queen to an illegal square
        self.assertFalse(self.make_move(game, 'd6', 'd5'))  # Black attempts to move their queen to an occupied square
        self.assertTrue(self.make_move(game, 'd6', 'b4'))  # Black moves their queen diagonally
        self.assertTrue(self.make_move(game, 'h3', 'c8'))  # White captures a black bishop
        self.assertTrue(self.make_move(game, 'b4', 'e1'))  # Black captures white's king
        self.assertFalse(self.make_move(game, 'g2', 'g4'))  # White attempts to make a move after black already won
        self.assertEqual(game.get_game_state(), GameState.BLACK_WON)  # Test correct game state

    def test_king_movement(self):
        """Test king movement."""
        game = Chess()
        self.assertTrue(self.make_move(game, 'e2', 'e4'))  # White moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'e7', 'e5'))  # Black moves a pawn two squares fwd
        self.assertFalse(self.make_move(game, 'e1', 'e3'))  # White attempts to move their king more than one square fwd
        self.assertFalse(self.make_move(game, 'e1', 'f1'))  # White attempts to move their king to an occupied square
        self.assertTrue(self.make_move(game, 'e1', 'e2'))  # White moves their king
        self.assertFalse(self.make_move(game, 'e8', 'f7'))  # Black attempts to move their king to an occupied square
        self.assertFalse(self.make_move(game, 'e8', 'e6'))  # Black attempts to move their king more than one square fwd
        self.assertTrue(self.make_move(game, 'e8', 'e7'))  # Black moves their king
        self.assertFalse(self.make_move(game, 'e2', 'g4'))  # White attempts to move their king to an illegal square
        self.assertTrue(self.make_move(game, 'e2', 'd3'))  # White moves their king diagonally
        self.assertTrue(self.make_move(game, 'e7', 'f6'))  # Black moves their king diagonally
        self.assertTrue(self.make_move(game, 'd3', 'd4'))  # White moves their king fwd
        self.assertTrue(self.make_move(game, 'f6', 'f5'))  # Black moves their king fwd
        self.assertTrue(self.make_move(game, 'd4', 'e5'))  # White captures a black pawn
        self.assertTrue(self.make_move(game, 'f5', 'e4'))  # Black captures a white pawn
        self.assertFalse(self.make_move(game, 'e5', 'e7'))  # White attempts to move their king two squares fwd
        self.assertTrue(self.make_move(game, 'e5', 'e4'))  # White captures black's king
        self.assertFalse(self.make_move(game, 'd8', 'e7'))  # Black attempts to make a move after white already won
        self.assertEqual(game.get_game_state(), GameState.WHITE_WON)  # Test correct game state

    def test_fairy_pieces(self):
        """Test entering fairy pieces and fairy piece movement."""
        game = Chess()
        self.assertTrue(self.make_move(game, 'd2', 'd4'))  # White moves a pawn two squares fwd
        self.assertTrue(self.make_move(game, 'g8', 'f6'))  # Black moves a knight
        self.assertTrue(self.make_move(game, 'c1', 'f4'))  # White moves a bishop
        self.assertTrue(self.make_move(game, 'e7', 'e6'))  # Black moves a pawn one square fwd
        self.assertTrue(self.make_move(game, 'f4', 'c7'))  # White captures a black pawn
        self.assertFalse(self.enter_fairy_piece(game, 'f', 'g8'))  # Black attempts to enter their falcon fairy piece
        self.assertTrue(self.make_move(game, 'f6', 'g4'))  # Black moves a knight
        self.assertTrue(self.make_move(game, 'c7', 'b8'))  # White captures a black knight
        self.assertFalse(self.enter_fairy_piece(game, 'F', 'g8'))  # Black attempts to enter the white falcon fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'f', 'f8'))  # Black attempts to enter their falcon fairy piece on an occupied square
        self.assertFalse(self.enter_fairy_piece(game, 'f', 'a6'))  # Black attempts to enter their falcon fairy piece outside their home ranks
        self.assertTrue(self.enter_fairy_piece(game, 'f', 'g8'))  # Black enters their falcon fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'F', 'c1'))  # White attempts to enter their fairy piece
        self.assertTrue(self.make_move(game, 'b1', 'c3'))  # White moves a knight
        self.assertTrue(self.make_move(game, 'a8', 'b8'))  # Black captures a white bishop
        self.assertFalse(self.enter_fairy_piece(game, 'f', 'd2'))  # White attempts to enter the black falcon fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'F', 'g2'))  # White attempts to enter their falcon fairy piece on an occupied square
        self.assertFalse(self.enter_fairy_piece(game, 'F','a3'))  # White attempts to enter their falcon fairy piece outside their home ranks
        self.assertTrue(self.enter_fairy_piece(game, 'F', 'd2'))  # White enters their falcon fairy piece
        self.assertFalse(self.make_move(game, 'd2', 'f4'))  # White attempts to take another turn
        self.assertFalse(self.make_move(game, 'g8', 'g5'))  # Black attempts to make their falcon move straight forward
        self.assertFalse(self.make_move(game, 'g8', 'e6'))  # Black attempts to make their falcon jump over another piece
        self.assertFalse(self.enter_fairy_piece(game, 'h', 'a8'))  # Black attempts to enter a second fairy piece
        self.assertTrue(self.make_move(game, 'f7', 'f5'))  # Black moves a pawn two squares fwd
        self.assertFalse(self.make_move(game, 'd2', 'd3'))  # White attempts to make their falcon move straight forward
        self.assertFalse(self.make_move(game, 'd2', 'c1'))  # White attempts to make their falcon move diagonally backwards
        self.assertFalse(self.make_move(game, 'd2', 'b4'))  # White attempts to make their falcon jump over another piece
        self.assertTrue(self.make_move(game, 'd2', 'h6'))  # White moves their falcon
        self.assertTrue(self.make_move(game, 'g7', 'h6'))  # Black captures white's falcon
        self.assertFalse(self.enter_fairy_piece(game, 'H', 'c1'))  # White attempts to enter a second fairy piece
        self.assertTrue(self.make_move(game, 'd1', 'd3'))  # White moves their queen
        self.assertTrue(self.make_move(game, 'f8', 'c5'))  # Black moves their bishop
        self.assertTrue(self.make_move(game, 'd4', 'c5'))  # White captures a black bishop
        self.assertFalse(self.enter_fairy_piece(game, 'H', 'c7'))  # Black attempts to enter the white hunter fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'f', 'c7'))  # Black attempts to enter a second falcon fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'h', 'a7'))  # Black attempts to enter their hunter fairy piece on an occupied square
        self.assertFalse(self.enter_fairy_piece(game, 'h', 'c6'))  # Black attempts to enter their hunter fairy piece outside their home ranks
        self.assertTrue(self.enter_fairy_piece(game, 'h', 'f7'))  # Black enters their hunter fairy piece
        self.assertFalse(self.make_move(game, 'f7', 'f6'))  # Black attempts to take another turn
        self.assertTrue(self.make_move(game, 'd3', 'f5'))  # White captures a black pawn
        self.assertTrue(self.make_move(game, 'e6', 'f5'))  # Black captures white's queen
        self.assertFalse(self.enter_fairy_piece(game, 'h', 'd2'))  # White attempts to enter the black hunter fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'F', 'd2'))  # White attempts to enter a second falcon fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'H', 'e1'))  # White attempts to enter their hunter fairy piece on an occupied square
        self.assertFalse(self.enter_fairy_piece(game, 'H','g3'))  # White attempts to enter their hunter fairy piece outside their home ranks
        self.assertTrue(self.enter_fairy_piece(game, 'H', 'd2'))  # White enters their hunter fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'h', 'c7'))  # Black attempts to enter another hunter fairy piece
        self.assertFalse(self.make_move(game, 'f7', 'd5'))  # Black attempts to move their hunter fairy piece diagonally forward
        self.assertFalse(self.make_move(game, 'f7', 'g6'))  # Black attempts to move their hunter fairy piece diagonally forward
        self.assertFalse(self.make_move(game, 'f7', 'f8'))  # Black attempts to move their hunter fairy piece straight backwards
        self.assertTrue(self.make_move(game, 'f7', 'f6'))  # Black moves their hunter fairy piece
        self.assertFalse(self.enter_fairy_piece(game, 'H', 'd1'))  # White attempts to enter another hunter fairy piece
        self.assertFalse(self.make_move(game, 'd2', 'e3'))  # White attempts to move their hunter fairy piece diagonally forward
        self.assertFalse(self.make_move(game, 'd2', 'd1'))  # White attempts to move their hunter fairy piece straight backwards
        self.assertTrue(self.make_move(game, 'd2', 'd7'))  # White moves their hunter fairy piece and captures a black pawn
        self.assertFalse(self.make_move(game, 'f6', 'c6'))  # Black attempts to move their hunter fairy piece sideways
        self.assertFalse(self.make_move(game, 'g8', 'f8'))  # Black attempts to move their falcon fairy piece sideways
        self.assertTrue(self.make_move(game, 'g8', 'b3'))  # Black moves their falcon
        self.assertTrue(self.make_move(game, 'c3', 'b5'))  # White moves a knight
        self.assertTrue(self.make_move(game, 'b3', 'b5'))  # Black captures a white knight
        self.assertTrue(self.make_move(game, 'd7', 'd8'))  # White captures black's queen
        self.assertTrue(self.make_move(game, 'e8', 'd8'))  # Black captures white's hunter


if __name__ == "__main__":
    unittest.main()
