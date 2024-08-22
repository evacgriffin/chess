# Test file for chess.py

import unittest
from chess import Chess


class TestChess(unittest.TestCase):
    """Contains unit tests for the Chess class"""
    def test_basic_make_move(self):
        """Test basic functionality of the make_move() method."""
        game = Chess()
        self.assertFalse(game.make_move('c3', 'c4'))  # Attempt to make a move from an empty start square
        self.assertFalse(game.make_move('f7', 'f5'))  # Attempt to move a piece that doesn't belong to the current player
        self.assertFalse(game.make_move('g1', 'i2'))  # Attempt to move a piece to a column that isn't on the board
        self.assertFalse(game.make_move('a1', 'Z1'))  # Attempt to move a piece to a column that isn't on the board
        self.assertFalse(game.make_move('e1', 'e0'))  # Attempt to move a piece to a row that isn't on the board
        self.assertFalse(game.make_move('g2', 'g9'))  # Attempt to move a piece to a row that isn't on the board
        self.assertFalse(game.make_move('h1', 'g1'))  # Attempt to move a piece to a square that already contains a piece by the current player

    def test_pawn_movement(self):
        """Test pawn movement."""
        game = Chess()
        self.assertTrue(game.make_move('c2', 'c4'))  # White moves two squares fwd
        self.assertTrue(game.make_move('d7', 'd5'))  # Black moves two squares fwd
        self.assertTrue(game.make_move('c4', 'd5'))  # White captures the black pawn
        self.assertFalse(game.make_move('h2', 'h3'))  # White tries to make another move
        self.assertTrue(game.make_move('g7', 'g6'))  # Black moves one square fwd
        self.assertTrue(game.make_move('f2', 'f4'))  # White moves two squares fwd
        self.assertTrue(game.make_move('f7', 'f5'))  # Black moves two squares fwd
        self.assertFalse(game.make_move('f4', 'f5'))  # White tries to capture by going straight fwd
        self.assertTrue(game.make_move('e2', 'e4'))  # White moves two squares fwd
        self.assertTrue(game.make_move('f5', 'e4'))  # Black captures a white pawn
        self.assertFalse(game.make_move('f4', 'f3'))  # White tries to move a pawn backwards
        self.assertTrue(game.make_move('a2', 'a3'))  # White moves pawn one square fwd
        self.assertFalse(game.make_move('e4', 'e5'))  # Black tries to move a pawn backwards
        self.assertTrue(game.make_move('e4', 'e3'))  # Black moves pawn one square fwd
        self.assertTrue(game.make_move('b2', 'b4'))  # White moves pawn two squares fwd
        self.assertFalse(game.make_move('e3', 'f4'))  # Black tries capturing backwards
        self.assertTrue(game.make_move('g6', 'g5'))  # Black moves pawn one square fwd
        self.assertTrue(game.make_move('d5', 'd6'))  # White moves pawn one square fwd
        self.assertTrue(game.make_move('g5', 'g4'))  # Black moves pawn one square fwd
        self.assertFalse(game.make_move('d6', 'c6'))  # White tries to move pawn one square sideways
        self.assertTrue(game.make_move('d6', 'e7'))  # White captures a black pawn
        self.assertTrue(game.make_move('g4', 'g3'))  # Black moves pawn one square fwd
        self.assertTrue(game.make_move('e7', 'd8'))  # White captures black's queen
        self.assertFalse(game.make_move('c7', 'd7'))  # Black tries to move pawn one square sideways
        self.assertFalse(game.make_move('b7', 'a6'))  # Black tries to move pawn diagonally fwd onto an empty square
        self.assertTrue(game.make_move('b7', 'b6'))  # Black moves pawn one square fwd
        self.assertFalse(game.make_move('g2', 'g4'))  # White tries to jump over a black pawn
        self.assertFalse(game.make_move('a3', 'a5'))  # White tries to move pawn two squares fwd when it is not the pawn's first turn
        self.assertFalse(game.make_move('d2', 'd5'))  # White tries to move pawn more than two squares on first turn
        self.assertFalse(game.make_move('b4', 'd6'))  # White tries to move pawn more than 1 space diagonally
        self.assertTrue(game.make_move('d2', 'd3'))  # White moves pawn one square fwd
        self.assertFalse(game.make_move('b6', 'b4'))  # Black tries to move pawn two squares fwd when it is not the pawn's first turn
        self.assertFalse(game.make_move('h7', 'h4'))  # Black tries to move pawn more than two squares on first turn
        self.assertFalse(game.make_move('c7', 'e5'))  # Black tries to move pawn more than 1 space diagonally
        self.assertTrue(game.make_move('c7', 'c5'))  # Black moves pawn one square fwd

    def test_knight_movement(self):
        """Test knight movement."""
        game = Chess()
        self.assertTrue(game.make_move('b1', 'a3'))  # White moves a knight
        self.assertTrue(game.make_move('g8', 'f6'))  # Black moves a knight
        self.assertTrue(game.make_move('g1', 'f3'))  # White moves a knight
        self.assertFalse(game.make_move('b8', 'b6'))  # Black tries to move a knight illegally
        self.assertTrue(game.make_move('b8', 'a6'))  # Black moves a knight
        self.assertFalse(game.make_move('a3', 'c2'))  # White tries to move a knight onto an occupied square
        self.assertFalse(game.make_move('a3', 'd4'))  # White tries to move a knight illegally
        self.assertTrue(game.make_move('a3', 'b5'))  # White moves a knight
        self.assertTrue(game.make_move('a6', 'b4'))  # Black moves a knight and jumps over a white knight
        self.assertTrue(game.make_move('b5', 'c7'))  # White moves a knight and captures a black pawn
        self.assertTrue(game.make_move('b4', 'a2'))  # Black moves a knight and captures a white pawn
        self.assertTrue(game.make_move('c7', 'e8'))  # White moves a knight and captures the black king
        self.assertFalse(game.make_move('a2', 'c1'))  # Black attempts to make a move after white already won
        self.assertEqual(game.get_game_state(), 'WHITE_WON')  # Test correct game state

    def test_bishop_movement(self):
        """Test bishop movement."""
        game = Chess()
        self.assertFalse(game.make_move('d7', 'd5'))  # Black attempts to move first
        self.assertTrue(game.make_move('g2', 'g4'))  # White moves a pawn two squares fwd
        self.assertTrue(game.make_move('d7', 'd5'))  # Black moves a pawn two squares fwd
        self.assertTrue(game.make_move('f1', 'h3'))  # White moves a bishop
        self.assertFalse(game.make_move('c8', 'a6'))  # Black attempts to make a bishop jump over a pawn
        self.assertTrue(game.make_move('c8', 'g4'))  # Black moves a bishop and captures a white pawn
        self.assertFalse(game.make_move('h3', 'h4'))  # White tries to move a bishop straight upwards
        self.assertTrue(game.make_move('h3', 'g4'))  # White captures a black bishop
        self.assertTrue(game.make_move('e7', 'e5'))  # Black moves a pawn two squares fwd
        self.assertTrue(game.make_move('g4', 'c8'))  # White moves a bishop
        self.assertTrue(game.make_move('f8', 'c5'))  # Black moves a bishop
        self.assertFalse(game.make_move('c8', 'a6'))  # White tries to move a bishop by jumping over a black pawn
        self.assertTrue(game.make_move('c8', 'e6'))  # White moves a bishop
        self.assertFalse(game.make_move('c5', 'a5'))  # Black tries to move a bishop sideways
        self.assertFalse(game.make_move('c5', 'a7'))  # Black tries to move a bishop to an occupied square
        self.assertTrue(game.make_move('c5', 'f2'))  # Black captures a white pawn
        self.assertFalse(game.make_move('e6', 'e8'))  # White tries to capture black's king with a bishop
        self.assertTrue(game.make_move('e6', 'f7'))  # White captures a black pawn
        self.assertTrue(game.make_move('f2', 'e1'))  # Black captures white's king
        self.assertFalse(game.make_move('f7', 'g8'))  # White attempts to make a move after black already won
        self.assertEqual(game.get_game_state(), 'BLACK_WON')  # Test correct game state

    def test_rook_movement(self):
        """Test rook movement."""
        game = Chess()
        self.assertTrue(game.make_move('a2', 'a4'))  # White moves a pawn two squares fwd
        self.assertFalse(game.make_move('h2', 'h4'))  # White attempts to go twice in a row
        self.assertTrue(game.make_move('b7', 'b5'))  # Black moves a pawn two squares fwd
        self.assertTrue(game.make_move('a4', 'b5'))  # White captures a black pawn
        self.assertTrue(game.make_move('h7', 'h5'))  # Black moves a pawn two squares fwd
        self.assertFalse(game.make_move('a1', 'b1'))  # White attempts to move a rook to an occupied square
        self.assertFalse(game.make_move('a1', 'c3'))  # White attempts to move a rook diagonally
        self.assertTrue(game.make_move('a1', 'a7'))  # White captures a black pawn with a rook
        self.assertFalse(game.make_move('h8', 'h4'))  # Black attempts to jump over another piece with a rook
        self.assertFalse(game.make_move('h8', 'h5'))  # Black attempts to move a rook to an occupied square
        self.assertTrue(game.make_move('a8', 'a7'))  # Black captures a white rook
        self.assertFalse(game.make_move('h1', 'h4'))  # White attempts to jump over another piece with a rook
        self.assertTrue(game.make_move('e2', 'e3'))  # White moves a pawn two squares fwd
        self.assertTrue(game.make_move('a7', 'a4'))  # Black moves a rook
        self.assertTrue(game.make_move('h2', 'h4'))  # White moves a pawn two squares fwd
        self.assertTrue(game.make_move('a4', 'h4'))  # Black captures a white pawn
        self.assertTrue(game.make_move('h1', 'h4'))  # White captures a black rook
        self.assertFalse(game.make_move('h8', 'f6'))  # Black attempts to move a rook diagonally
        self.assertTrue(game.make_move('h8', 'h6'))  # Black moves a rook
        self.assertTrue(game.make_move('h4', 'e4'))  # White moves a rook
        self.assertFalse(game.make_move('h6', 'e3'))  # Black attempts to capture a white pawn by moving diagonally
        self.assertTrue(game.make_move('h6', 'e6'))  # Black moves a rook
        self.assertTrue(game.make_move('e4', 'e6'))  # White moves a rook
        self.assertTrue(game.make_move('h5', 'h4'))  # Black moves a pawn one square fwd
        self.assertTrue(game.make_move('e6', 'e7'))  # White captures a black pawn
        self.assertTrue(game.make_move('h4', 'h3'))  # Black moves a pawn one square fwd
        self.assertTrue(game.make_move('e7', 'e8'))  # White captures black's king
        self.assertFalse(game.make_move('h3', 'h2'))  # Black attempts to make a move after white already won
        self.assertEqual(game.get_game_state(), 'WHITE_WON')  # Test correct game state

    def test_queen_movement(self):
        """Test queen movement."""
        game = Chess()
        self.assertFalse(game.make_move('d1', 'd3'))  # White attempts to make their queen jump over another piece
        self.assertTrue(game.make_move('d2', 'd4'))  # White moves a pawn two squares fwd
        self.assertFalse(game.make_move('d8', 'd6'))  # Black attempts to make their queen jump over another piece
        self.assertTrue(game.make_move('d7', 'd5'))  # Black moves a pawn two squares fwd
        self.assertTrue(game.make_move('d1', 'd3'))  # White moves their queen
        self.assertTrue(game.make_move('d8', 'd6'))  # Black moves their queen
        self.assertFalse(game.make_move('d3', 'g4'))  # White attempts to move their queen to an illegal square
        self.assertFalse(game.make_move('d3', 'e2'))  # White attempts to move their queen to an occupied square
        self.assertTrue(game.make_move('d3', 'h3'))  # White moves their queen
        self.assertFalse(game.make_move('d6', 'c3'))  # Black attempts to move their queen to an illegal square
        self.assertFalse(game.make_move('d6', 'd5'))  # Black attempts to move their queen to an occupied square
        self.assertTrue(game.make_move('d6', 'b4'))  # Black moves their queen diagonally
        self.assertTrue(game.make_move('h3', 'c8'))  # White captures a black bishop
        self.assertTrue(game.make_move('b4', 'e1'))  # Black captures white's king
        self.assertFalse(game.make_move('g2', 'g4'))  # White attempts to make a move after black already won
        self.assertEqual(game.get_game_state(), 'BLACK_WON')  # Test correct game state

    def test_king_movement(self):
        """Test king movement."""
        game = Chess()
        self.assertTrue(game.make_move('e2', 'e4'))  # White moves a pawn two squares fwd
        self.assertTrue(game.make_move('e7', 'e5'))  # Black moves a pawn two squares fwd
        self.assertFalse(game.make_move('e1', 'e3'))  # White attempts to move their king more than one square fwd
        self.assertFalse(game.make_move('e1', 'f1'))  # White attempts to move their king to an occupied square
        self.assertTrue(game.make_move('e1', 'e2'))  # White moves their king
        self.assertFalse(game.make_move('e8', 'f7'))  # Black attempts to move their king to an occupied square
        self.assertFalse(game.make_move('e8', 'e6'))  # Black attempts to move their king more than one square fwd
        self.assertTrue(game.make_move('e8', 'e7'))  # Black moves their king
        self.assertFalse(game.make_move('e2', 'g4'))  # White attempts to move their king to an illegal square
        self.assertTrue(game.make_move('e2', 'd3'))  # White moves their king diagonally
        self.assertTrue(game.make_move('e7', 'f6'))  # Black moves their king diagonally
        self.assertTrue(game.make_move('d3', 'd4'))  # White moves their king fwd
        self.assertTrue(game.make_move('f6', 'f5'))  # Black moves their king fwd
        self.assertTrue(game.make_move('d4', 'e5'))  # White captures a black pawn
        self.assertTrue(game.make_move('f5', 'e4'))  # Black captures a white pawn
        self.assertFalse(game.make_move('e5', 'e7'))  # White attempts to move their king two squares fwd
        self.assertTrue(game.make_move('e5', 'e4'))  # White captures black's king
        self.assertFalse(game.make_move('d8', 'e7'))  # Black attempts to make a move after white already won
        self.assertEqual(game.get_game_state(), 'WHITE_WON')  # Test correct game state

    def test_fairy_pieces(self):
        """Test entering fairy pieces and fairy piece movement."""
        game = Chess()
        self.assertTrue(game.make_move('d2', 'd4'))  # White moves a pawn two squares fwd
        self.assertTrue(game.make_move('g8', 'f6'))  # Black moves a knight
        self.assertTrue(game.make_move('c1', 'f4'))  # White moves a bishop
        self.assertTrue(game.make_move('e7', 'e6'))  # Black moves a pawn one square fwd
        self.assertTrue(game.make_move('f4', 'c7'))  # White captures a black pawn
        self.assertFalse(game.enter_fairy_piece('f', 'g8'))  # Black attempts to enter their falcon fairy piece
        self.assertTrue(game.make_move('f6', 'g4'))  # Black moves a knight
        self.assertTrue(game.make_move('c7', 'b8'))  # White captures a black knight
        self.assertFalse(game.enter_fairy_piece('F', 'g8'))  # Black attempts to enter the white falcon fairy piece
        self.assertFalse(game.enter_fairy_piece('f', 'f8'))  # Black attempts to enter their falcon fairy piece on an occupied square
        self.assertFalse(game.enter_fairy_piece('f', 'a6'))  # Black attempts to enter their falcon fairy piece outside their home ranks
        self.assertTrue(game.enter_fairy_piece('f', 'g8'))  # Black enters their falcon fairy piece
        self.assertFalse(game.enter_fairy_piece('F', 'c1'))  # White attempts to enter their fairy piece
        self.assertTrue(game.make_move('b1', 'c3'))  # White moves a knight
        self.assertTrue(game.make_move('a8', 'b8'))  # Black captures a white bishop
        self.assertFalse(game.enter_fairy_piece('f', 'd2'))  # White attempts to enter the black falcon fairy piece
        self.assertFalse(game.enter_fairy_piece('F', 'g2'))  # White attempts to enter their falcon fairy piece on an occupied square
        self.assertFalse(game.enter_fairy_piece('F','a3'))  # White attempts to enter their falcon fairy piece outside their home ranks
        self.assertTrue(game.enter_fairy_piece('F', 'd2'))  # White enters their falcon fairy piece
        self.assertFalse(game.make_move('d2', 'f4'))  # White attempts to take another turn
        self.assertFalse(game.make_move('g8', 'g5'))  # Black attempts to make their falcon move straight forward
        self.assertFalse(game.make_move('g8', 'e6'))  # Black attempts to make their falcon jump over another piece
        self.assertFalse(game.enter_fairy_piece('h', 'a8'))  # Black attempts to enter a second fairy piece
        self.assertTrue(game.make_move('f7', 'f5'))  # Black moves a pawn two squares fwd
        self.assertFalse(game.make_move('d2', 'd3'))  # White attempts to make their falcon move straight forward
        self.assertFalse(game.make_move('d2', 'c1'))  # White attempts to make their falcon move diagonally backwards
        self.assertFalse(game.make_move('d2', 'b4'))  # White attempts to make their falcon jump over another piece
        self.assertTrue(game.make_move('d2', 'h6'))  # White moves their falcon
        self.assertTrue(game.make_move('g7', 'h6'))  # Black captures white's falcon
        self.assertFalse(game.enter_fairy_piece('H', 'c1'))  # White attempts to enter a second fairy piece
        self.assertTrue(game.make_move('d1', 'd3'))  # White moves their queen
        self.assertTrue(game.make_move('f8', 'c5'))  # Black moves their bishop
        self.assertTrue(game.make_move('d4', 'c5'))  # White captures a black bishop
        self.assertFalse(game.enter_fairy_piece('H', 'c7'))  # Black attempts to enter the white hunter fairy piece
        self.assertFalse(game.enter_fairy_piece('f', 'c7'))  # Black attempts to enter a second falcon fairy piece
        self.assertFalse(game.enter_fairy_piece('h', 'a7'))  # Black attempts to enter their hunter fairy piece on an occupied square
        self.assertFalse(game.enter_fairy_piece('h', 'c6'))  # Black attempts to enter their hunter fairy piece outside their home ranks
        self.assertTrue(game.enter_fairy_piece('h', 'f7'))  # Black enters their hunter fairy piece
        self.assertFalse(game.make_move('f7', 'f6'))  # Black attempts to take another turn
        self.assertTrue(game.make_move('d3', 'f5'))  # White captures a black pawn
        self.assertTrue(game.make_move('e6', 'f5'))  # Black captures white's queen
        self.assertFalse(game.enter_fairy_piece('h', 'd2'))  # White attempts to enter the black hunter fairy piece
        self.assertFalse(game.enter_fairy_piece('F', 'd2'))  # White attempts to enter a second falcon fairy piece
        self.assertFalse(game.enter_fairy_piece('H', 'e1'))  # White attempts to enter their hunter fairy piece on an occupied square
        self.assertFalse(game.enter_fairy_piece('H','g3'))  # White attempts to enter their hunter fairy piece outside their home ranks
        self.assertTrue(game.enter_fairy_piece('H', 'd2'))  # White enters their hunter fairy piece
        self.assertFalse(game.enter_fairy_piece('h', 'c7'))  # Black attempts to enter another hunter fairy piece
        self.assertFalse(game.make_move('f7', 'd5'))  # Black attempts to move their hunter fairy piece diagonally forward
        self.assertFalse(game.make_move('f7', 'g6'))  # Black attempts to move their hunter fairy piece diagonally forward
        self.assertFalse(game.make_move('f7', 'f8'))  # Black attempts to move their hunter fairy piece straight backwards
        self.assertTrue(game.make_move('f7', 'f6'))  # Black moves their hunter fairy piece
        self.assertFalse(game.enter_fairy_piece('H', 'd1'))  # White attempts to enter another hunter fairy piece
        self.assertFalse(game.make_move('d2', 'e3'))  # White attempts to move their hunter fairy piece diagonally forward
        self.assertFalse(game.make_move('d2', 'd1'))  # White attempts to move their hunter fairy piece straight backwards
        self.assertTrue(game.make_move('d2', 'd7'))  # White moves their hunter fairy piece and captures a black pawn
        self.assertFalse(game.make_move('f6', 'c6'))  # Black attempts to move their hunter fairy piece sideways
        self.assertFalse(game.make_move('g8', 'f8'))  # Black attempts to move their falcon fairy piece sideways
        self.assertTrue(game.make_move('g8', 'b3'))  # Black moves their falcon
        self.assertTrue(game.make_move('c3', 'b5'))  # White moves a knight
        self.assertTrue(game.make_move('b3', 'b5'))  # Black captures a white knight
        self.assertTrue(game.make_move('d7', 'd8'))  # White captures black's queen
        self.assertTrue(game.make_move('e8', 'd8'))  # Black captures white's hunter


if __name__ == '__main__':
    unittest.main()
