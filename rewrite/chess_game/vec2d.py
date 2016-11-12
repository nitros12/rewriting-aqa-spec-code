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
