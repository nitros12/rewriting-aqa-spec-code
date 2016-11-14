import chess_game as cg

if __name__ == "__main__":
    board = cg.GameBoard("game", 8, 8)
    board.add_pieces(cg.King(0, 0, "W"), cg.King(0, 1, "B"))
    board.run_game()
