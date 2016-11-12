from .vec2d import vec2d

class move(object):
    def __init__(self, piece, board, start, end):
        self.piece = piece
        self.board = board
        self.start = start
        self.end = end
        self.valid = self.run_validation()
        self.taken = self.piece.test_take(self.board, self) if self.valid else False

    def __str__(self):
        return "Move: (piece: {0.piece}, board: {0.board}, start: {0.start}, end: {0.end} (valid: {0.valid}, take: {0.taken}))".format(self)

    def run_validation(self):
        return self.piece.validate_move(self.board, self)

    def run_move(self):
        if self.valid:
            self.piece.set_loc(self.end)

class game_state(object):
    def __init__(self):
        self.turn = "W"
        self.white_takes = 0
        self.black_takes = 0
        self.turns = 0

    def __str__(self):
        return "game_state: (Turn: {0.turn}, white_takes: {0.white_takes}, black_takes: {0.black_takes}, Turns completed: {0.turns})".format(self)

    def swap_turn(self):
        self.turn = {"W":"B", "B":"W"}[self.turn]

    def inc_turns(self):
        self.turns += 1

    def add_take(self):
        if self.turn == "W":
            self.white_takes  += 1
        else:
            self.black_takes += 1



class game_board(object):
    '''holds game objects
    game is run from here'''
    def __init__(self, name :str):
        self.name = name
        self.pieces = []
        self.state = game_state()

    def __str__(self):
        return "Board: (name: {0.name}, state: {0.state}, pieces: {1})".format(self, ', '.join([str(i) for i in self.pieces]))

    def set_pieces(self, pieces):
        self.pieces = pieces

    def add_pieces(self, *pieces):
        for piece in pieces:
            self.pieces.append(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def check_pieces(self, *locations):
        return list(filter(lambda x: x.check_self_locations(*locations), self.pieces))

    def find_piece(self, location):
        pieces = self.check_pieces(location)
        if len(pieces) > 1:
            raise Exception("multiple pieces occupy same location: {0}: [{1}]".format(location, ', '.join(pieces)))
        elif pieces:
            return pieces[0]
        else:
            return

    def construct_move(self, piece, start, end):
        return move(piece, self, start, end)

    def run_take(self, take):
        print("took piece: {}".format(take.taken))
        self.state.add_take()
        self.remove_piece(take.taken)

    def runGame(self):
        while True:
            while True:
                start = wait_for_valid("Piece to move (in format: x,y): ", lambda x: len(x.split(",")) == 2, lambda x: vec2d(*[int(i.strip()) for i in x.split(",")]))
                # grab piece
                piece = self.find_piece(start)
                if not piece:
                    print("there was no piece there, please enter a valid piece!")
                elif not piece.test_owner(self.state.turn):
                    print("You cannot move a piece that is owned by an enemy")
                else:
                    break
            print("picked piece: {}".format(piece))
            end = wait_for_valid("Place to move to: (in format x,y): ", lambda x: len(x.split(",")) == 2, lambda x: vec2d(*[int(i.strip()) for i in x.split(",")]))
            movePiece = self.construct_move(piece, start, end)
            print(movePiece)
            if movePiece.valid:
                break
            print("move is invalid!") # Todo: give reason
        if movePiece.taken:
            self.run_take(movePiece.taken)
        movePiece.run_move()
        self.state.inc_turns()
        self.state.swap_turn()

def wait_for_valid(question :str, test = (lambda x: x), formatter = (lambda x: x)):
    temp = ""
    while not test(temp):
        temp = input(question)
    return formatter(temp)
