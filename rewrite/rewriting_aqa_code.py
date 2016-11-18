import chess_game as cg
from chess_game.vec2d import Vec2D

if __name__ == "__main__":
    board = cg.GameBoard("game", 8, 8)
    board.add_pieces(cg.King(8, 8, "B"), cg.King(4, 4, "B"),
                     cg.Bishop(0, 0, "W"))
    board.run_game()
