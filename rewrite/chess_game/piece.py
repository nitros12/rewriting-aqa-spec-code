from .vec2d import Vec2D


class Take(object):
    def __init__(self, capturer, taken):
        self.capturer = capturer
        self.taken = taken

    def __str__(self):
        return "Take: (capturer: {0.capturer} taking: {0.taken})".format(self)


class Piece(object):
    def __init__(self, x, y, name, owner):
        self.location = Vec2D(x, y)
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

    @staticmethod
    def test_take(board, move):
        piece = board.find_piece(move.end)  # type: Piece
        if not piece:
            print("false at if not piece")
            return False
        elif piece.test_owner(move.piece.owner):
            print("false at test_owner")
            return False
        return Take(move.piece, piece)


class SomePiece(Piece):
    def __init__(self, x, y, owner):
        super().__init__(x, y, "somepiece", owner)
        self.kernel = [
            Vec2D(1, 0),
            Vec2D(0, 1),
            Vec2D(-1, 0),
            Vec2D(0, -1)
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
            # not in valid location, stop now
        return super().validate_move(board, move)
