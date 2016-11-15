import chess_game as cg
from chess_game.vec2d import Vec2D

if __name__ == "__main__":
    print(Vec2D(10,0) % Vec2D(3, 1))

    board = cg.GameBoard("game", 8, 8)
    board.add_pieces(cg.King(0, 0, "W"), cg.King(0, 1, "B"),
                     cg.Bishop(1, 0, "W"))
    board.run_game()
