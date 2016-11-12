from .vec2d import vec2d

class take(object):
    def __init__(self, capturer, taken):
        self.capturer = capturer
        self.taken = taken

    def __str__(self):
        return "Take: (capturer: {0.capturer} taking: {0.taken})".format(self)

class piece(object):
    def __init__(self, x, y, name, owner):
        self.location = vec2d(x,y)
        self.name = name
        self.owner = owner

    def __str__(self):
        return "Piece: (owner: {0.owner}, type: {0.name} in position {0.location})".format(self)

    def test_owner(self, owner):
        return self.owner == owner

    def get_loc(self):
        return self.location

    def set_loc(self, newloc):
        self.location = newloc

    def get_loc_xy(self):
        return self.location.x, self.location.y

    def test_location(self, location):
        if self.location == location:
            return self # return self if at location

    def check_self_locations(self, *locations):
        return self.location in locations

    def validate_move(self, board, move):
        test_piece = board.find_piece(move.end)
        if not test_piece:
            return True # nothing in way, go ahead
        # grab teams
        if test_piece.test_owner(move.piece.owner):
            return False
            # cannot move onto your own piece
        else:
            # piece is of enemy team
            return True

        # return none if fallen out

    def test_take(self, board, move):
        piece = board.find_piece(move.end) # type: piece
        if not piece:
            print("false at if not piece")
            return False
        elif piece.test_owner(move.piece.owner):
            print("false at test_owner")
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
