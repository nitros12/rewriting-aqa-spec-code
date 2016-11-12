import chess_game as cg

if __name__ == "__main__":
    board = cg.game_board("game")
    board.add_pieces(cg.somepiece(0, 0, "W"), cg.somepiece(0, 1, "B"))
    board.runGame()
