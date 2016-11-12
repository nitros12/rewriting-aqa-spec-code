import chess_game as cg

if __name__ == "__main__":
    board = cg.GameBoard("game")
    board.add_pieces(cg.SomePiece(0, 0, "W"), cg.SomePiece(0, 1, "B"))
    board.run_game()
