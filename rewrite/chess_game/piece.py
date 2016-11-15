from .vec2d import Vec2D


class Take(object):
    def __init__(self, capturer, taken):
        self.capturer = capturer
        self.taken = taken

    def __str__(self):
        return "Take: (capturer: {0.capturer} taking: {0.taken})".format(self)


class Piece(object):
    def __init__(self, x, y, name, owner):
        self._location = Vec2D(x, y)
        self.name = name
        self.owner = owner

    def __str__(self):
        return "Piece: (owner: {0.owner}, type: {0.name} in position {0.location})".format(self)

    def test_owner(self, owner):
        return self.owner == owner

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, xy, y=None):
        if isinstance(xy, Vec2D):
            self._location = xy
        elif isinstance(xy, int) and isinstance(y, int):
            self._location = Vec2D(xy, y)
        else:
            raise Exception("Cannot set location to that!")

    def test_location(self, location):
        if self._location == location:
            return self # return self if at location

    def check_self_locations(self, *locations):
        return self._location in locations

    @staticmethod
    def validate_move(board, move):
        if board.game_size not in move.end:
            #  reversed operators because???
            return False
        test_piece = board.find_piece(move.end)
        if not test_piece:
            return True  # nothing in way, go ahead
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
            #  no pieces to take
            return False
        elif piece.test_owner(move.piece.owner):
            #  piece is on same team
            return False
        return Take(move.piece, piece)


class FixedPiece(Piece):
    '''A piece that can only move N amount at once
    (Unlike a chess queen which can move any value of pieces unless blocked'''
    def __init__(self, x, y, name, owner, kernel):
        super().__init__(x, y, name, owner)
        self.kernel = kernel

    def validate_kernel(self, move):
        for i in self.kernel:
            if self._location + i == move.end:
                return True
        return False

    def validate_move(self, board, move):
        # first ensure that moved to valid locations
        if not self.validate_kernel(move):
            return False
            # not in valid location, stop now
        return super().validate_move(board, move)


class MovePiece(Piece):
    '''A piece that can move any amount in a given direction,
    providing it the new position is not blocked by a piece'''
    def __init__(self, x, y, name, owner, kernel):
        super().__init__(x, y, name, owner)
        self.kernel = kernel

    def validate_kernel(self, move):
        for i in self.kernel:
            if move.calculate_movement(i):
                return i
        return False
        #  not moving down valid path

    def validate_move(self, board, move):
        valid_kernel = self.validate_kernel(move)
        if not valid_kernel:
            return False

        print("Valid: " + str(valid_kernel))

        for i in range(abs(move.end.x - move.start.x) if valid_kernel.x else abs(move.end.y - self.y)):
            if board.find_piece(move.start + valid_kernel * Vec2D(i, i)):
                return False

        return super().validate_move(board, move)


class King(FixedPiece):
    '''A king piece'''
    def __init__(self, x, y, owner):
        kernel = [
            Vec2D(1, 0),
            Vec2D(1, 1),
            Vec2D(0, 1),
            Vec2D(-1, 1),
            Vec2D(-1, 0),
            Vec2D(-1, -1),
            Vec2D(0, -1),
            Vec2D(1, -1)
            ]
        super().__init__(x, y, "King", owner, kernel)


class Bishop(MovePiece):
    def __init__(self, x, y, owner):
        kernel = [
                Vec2D(1,1),
                Vec2D(-1,1),
                Vec2D(-1,-1),
                Vec2D(1,-1)
        ]
        super().__init__(x, y, "Bishop", owner, kernel)




