from .vec2d import Vec2D
from enum import Enum

class teams(Enum):
    white = "W"
    black = "B"

class GameException:
    def __bool__(self):
        return False  # y tho


class KingInCheck:
    def __bool__(self):
        return False

    def __init__(self, taker, king, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taker = taker
        self.king = king


class Take:
    def __init__(self, capturer, taken):
        self.capturer = capturer
        self.taken = taken

    def __str__(self):
        return "Take: (capturer: {0.capturer} taking: {0.taken})".format(self)


class Piece:
    def __init__(self, x, y, name, owner):
        self._location = Vec2D(x, y)
        self.name = name
        self.owner = owner

    def __str__(self):
        return "Piece: (owner: {0.owner}, type: {0.name} in position {0.location})".format(self)

    def test_owner(self, owner):
        return self.owner is owner

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

    def test_self_type(self, piece_type):
        return isinstance(self, piece_type)

    def allowed_to_take(self, taker):
        return True

    def validate_move(self, board, move):
        if board.game_size not in move.end:
            #  reversed operators because???
            return GameException("Cannot move out of bounds")
        test_piece = board.find_piece(move.end)
        if not test_piece:
            return True  # nothing in way, go ahead
        # grab teams
        elif test_piece.test_owner(move.piece.owner):
            return GameException("Cannot move onto member of your own team")
            # cannot move onto your own piece
        else:
            # piece is of enemy team
            return test_piece.allowed_to_take(self)
        # return none if fallen out

    @staticmethod
    def test_take(board, move):
        piece = board.find_piece(move.end)  # type: Piece
        if not piece:
            #  no pieces to take
            return GameException("No piece to take")
        elif piece.test_owner(move.piece.owner):
            #  piece is on same team
            return GameException("Piece to take on same team")
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
            if move.test_signs(i):
                return i
        return False
        #  not moving down valid path

    def validate_move(self, board, move):
        movement = move.end - move.start

        valid_kernel = self.validate_kernel(movement)  # Type: Vec2D
        if not valid_kernel:
            return False

        print("Valid: " + str(valid_kernel))

        for i in range(1, abs(move.end.x - move.start.x)-1):
            # next piece to location before last
            found_piece = board.find_piece(move.start + valid_kernel * Vec2D(i, i))
            if found_piece and found_piece is not self:  # if any piece on way on journey, ignore it
                print("invalid piece = {}".format(found_piece))
                return GameException("Attempt to jump over another piece")

        print("still valid")

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

    def allowed_to_take(self, taker):
        return KingInCheck(taker, self, "You cannot take the king.")


class Bishop(MovePiece):
    def __init__(self, x, y, owner):
        kernel = [
                Vec2D(1,1),
                Vec2D(-1,1),
                Vec2D(-1,-1),
                Vec2D(1,-1)
        ]
        super().__init__(x, y, "Bishop", owner, kernel)

    def validate_move(self, board, move):
        movement = move.end - move.start
        if not abs(movement).isequal():
            return False

        return super().validate_move(board, move)

class Queen(MovePiece):
    def __init__(self, x, y, owner):
        kernel = [
                Vec2D(1,1),
                Vec2D(-1,1),
                Vec2D(-1,-1),
                Vec2D(1,-1),
        ]
        super().__init__(x, y, "Bishop", owner, kernel)

    def validate_move(self, board, move):
        movement = move.end - move.start # type: Vec2D
        if not (abs(movement).isequal() or movement.either(0)):
            return False

        return super().validate_move(board, move)

class Rook(MovePiece):
    def __init__(self, x, y, owner):
        kernel = [
                Vec2D(1,1),
                Vec2D(-1,1),
                Vec2D(-1,-1),
                Vec2D(1,-1)
        ]
        super().__init__(x, y, "Bishop", owner, kernel)

    def validate_move(self, board, move):
        movement = move.end - move.start # type: Vec2D
        if not movement.either(0):
            return False

        return super().validate_move(board, move)
