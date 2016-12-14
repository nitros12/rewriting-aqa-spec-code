import chess_game as cg
from chess_game.vec2d import Vec2D


if __name__ == "__main__":
    board = cg.GameBoard("game", 8, 8)
    board.add_pieces(cg.King(8, 8, cg.teams.white), cg.King(4, 4, cg.teams.black),
                     cg.Bishop(0, 0, cg.teams.black))
    board.run_game()
