class Block:
    def __init__(self, x, y, f, g, h, star, previous):
        self.x = x
        self.y = y
        self.f = f
        self.g = g
        self.h = h
        self.star = star
        self.previous = previous
