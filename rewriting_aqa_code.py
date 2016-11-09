class pieces(object):
    def __init__(self):
        self.piece_dict = {}
        
    def piece(self, func):
        def predicate():
            self.piece_dict[func.__name__] = func

        return predicate
    return func


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

    def get_loc(self):
        return self.location

    def get_loc_xy(self):
        return self.location.x, self.location.y

    def test_location(self, location):
        if self.location == location:
            return self # return self if at location

    def check_self_locations(self, *locations):
        return not all(map(lambda x: self.location == x, locations))



class somepiece(piece):
    def __init__(self, x, y, owner):
        super().__init__(x, y, "somepiece", owner)

    def validate_move(self, board):
        
        


class game_board(object):
    def __init__(self, name :str):
        self.name = name
        self.pieces = []

    def set_pieces(self, pieces):
        self.pieces = pieces

    def add_piece(self, piece):
        self.pieces.append(piece)

    def check_pieces(self, location):
        pieces = filter(lambda x: x.check_self_locations(*locations), self.pieces) 
        
        
