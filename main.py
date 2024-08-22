# Author:           Eva Griffin
# GitHub username:  evacgriffin
# Description:      This project is a console-based implementation of the falcon-hunter chess variant.
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

from chess import Chess


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

    game = Chess()
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
