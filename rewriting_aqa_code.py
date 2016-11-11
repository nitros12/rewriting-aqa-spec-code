class vec2d(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, vec):
        try:
            return vec2d(
                self.x + vec.x,
                self.y + vec.y)
        except:
            raise ValueError("cannot add non type vec2d to vec2d")

    def __sub__(self, vec):
        try:
            return vec2d(
                self.x - vec.x,
                self.y - vec.y)
        except:
            raise ValueError("cannot sub non type vec2d from vec2d")

    def __eq__(self, vec):
        return self.x == vec.x and self.y == vec.y

    def __str__(self):
        return "x: {0.x}, y: {0.y}".format(self)

class piece(object):
    def __init__(self, x, y, name, owner):
        self.location = vec2d(x,y)
        self.name = name
        self.owner = owner

    def test_owner(self, owner):
        return self.owner == owner

    def get_loc(self):
        return self.location

    def get_loc_xy(self):
        return self.location.x, self.location.y

    def test_location(self, location):
        if self.location == location:
            return self # return self if at location

    def check_self_locations(self, *locations):
        return self.location in locations

    def validate_move(self, board, move):
        test_piece = board.check_pieces(move.end)
        if not test_piece:
            return True # nothing in way, go ahead
        # grab teams
        if test_piece.test_owner(move.piece.owner):
            return False
            # cannot move onto your own piece

    def test_take(self, board, move):
        piece = board.check_pieces(move.end) # type: piece
        if not piece:
            return False
        elif piece.check_owner(move.piece.owner):
            return False
        return take(move.piece, piece)


class somepiece(piece):
    def __init__(self, x, y, owner):
        super().__init__(x, y, "somepiece", owner)
        self.kernel = [
            vec2d(1,0),
            vec2d(0,1),
            vec2d(-1,0),
            vec2d(0,-1)
        ]

    def validate_kernel(self, move):
        for i in self.kernel:
            if self.location + i == move.end:
                return True
        return False

    def validate_move(self, board, move):
        # first ensure that moved to valid locations
        if not self.validate_kernel(move):
            return False
            # not in valid location, stop noew
        return super().validate_move(board, move)



class move(object):
    def __init__(self, piece :piece, board, start :vec2d, to :vec2d):
        self.piece = piece
        self.board = board
        self.start = start
        self.end = to
        self.valid = True
        self.taken = False

    def __str__(self):
        return "piece: {0.piece}, board: {0.board}, start: {0.start}, end: {0.end}".format(self)

    def run_validation(self):
        self.valid = self.piece.validate_move(self.board, self)
        if self.valid:
            self.taken = self.piece.test_take(self.board, self)

class take(object):
    def __init__(self, capturer :piece, taken :piece):
        self.capturer = capturer
        self.taken = taken

class game_state(object):
    def __init__(self):
        self.turn = "W"
        self.white_takes = 0
        self.black_takes = 0
        self.turns = 0

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
    def __init__(self, name :str):
        self.name = name
        self.pieces = []
        self.state = game_state()

    def set_pieces(self, pieces):
        self.pieces = pieces

    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def check_pieces(self, location):
        return filter(lambda x: x.check_self_locations(*locations), self.pieces)

    def construct_move(self, piece, start, end):
        return move(piece, self, start, end)

    def run_take(self, take):
        print("took piece: {}".format(take.taken))
        self.state.add_take()
        self.remove_piece(take.taken)

    def runGame(self):
        while True:
            while True:
                start = wait_for_valid("Piece to move (in format: x,y)", lambda x: len(x.split(",")) == 2, lambda x: vec2d(*[int(i.strip()) for i in x.split(",")]))
                # grab piece
                piece = self.check_pieces(start)
                if not piece:
                    print("there was no piece there, please enter a valid piece!")
                else:
                    break
            end = wait_for_valid("Place to move to: (in format x,y)", lambda x: len(x.split(",")) == 2, lambda x: vec2d(*[int(i.strip()) for i in x.split(",")]))
            movePiece = self.construct_move(piece, start, end)
            print(movePiece)
            movePiece.run_validation()
            if movePiece.valid:
                break
            print("move is invalid!") # Todo: give reason
        if movePiece.taken:
            self.run_take(movePiece.taken)
        self.state.inc_turns()
        self.state.swap_turn()

def wait_for_valid(question :str, test, formatter = (lambda x: x)):
    temp = ""
    while not test(temp):
        temp = input(question)
    return formatter(temp)
