class Vec2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isequal(self):
        return self.x == self.y

    def sign(self):
        return abs(self)/self

    def test_signs(self, signs):
        return self.sign() == signs

    def either(self, num):
        return (self.x == num or self.y == num) and not self.x == self.y

    def __add__(self, other):
        try:
            return Vec2D(
                self.x + other.x,
                self.y + other.y)
        except:
            raise ValueError("cannot add non type vec2d to vec2d")
    __radd__ = __add__

    def __sub__(self, other):
        try:
            return Vec2D(
                self.x - other.x,
                self.y - other.y)
        except:
            raise ValueError("cannot sub non type vec2d from vec2d")

    def __mul__(self, other):
        try:
            return Vec2D(
                self.x * other.x,
                self.y * other.y)
        except:
            raise ValueError("cannot multiply non type vec2d with vec2d")

    def __truediv__(self, other):
        try:
            return Vec2D(
                self.x / other.x,
                self.y / other.y)
        except:
            raise ValueError("cannot divide non type vec2d by vec2d")

    def __floordiv__(self, other):
        try:
            return Vec2D(
                self.x // other.x,
                self.y // other.y)
        except:
            raise ValueError("cannot divide non type vec2d by vec2d")

    def __eq__(self, vec):
        return self.x == vec.x and self.y == vec.y

    def __str__(self):
        return "x: {0.x}, y: {0.y}".format(self)

    def __mod__(self, other):
        '''modulus, avoids modulus by 0 by returning 0'''
        return Vec2D(self.x % other.x if other.x else 0, self.y % other.y if other.y else 0)

    def __contains__(self, item):
        return self.x in range(item.x+1) and self.y in range(item.y+1)

    def __not__(self):
        return not (self.x and self.y)

    def __bool__(self):
        return bool(self.x and self.y)

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return Vec2D(abs(self.x), abs(self.y))
