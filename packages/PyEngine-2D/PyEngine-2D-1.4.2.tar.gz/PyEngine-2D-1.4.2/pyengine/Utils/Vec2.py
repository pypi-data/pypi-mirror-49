import math
from typing import Tuple

__all__ = ["Vec2"]


class Vec2:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    @property
    def coords(self) -> Tuple[int, int]:
        return self.x, self.y

    @coords.setter
    def coords(self, dic: Tuple[int, int]) -> None:
        self.x = dic[0]
        self.y = dic[1]

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    @length.setter
    def length(self, value):
        pass

    def normalized(self):
        if self.length == 0:
            return Vec2(0, 0)
        else:
            return Vec2(int(self.x / self.length), int(self.y / self.length))

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        else:
            return Vec2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        else:
            return Vec2(self.x - other, self.y - other)

    def __rsub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(other.x - self.x, other.y - self.y)
        else:
            return Vec2(other - self.x, other - self.y)

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        else:
            return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vec2):
            return Vec2(int(self.x / other.x), int(self.y / other.y))
        else:
            return Vec2(int(self.x / other), int(self.y / other))

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return "Vec2"+str(self.coords)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Vec2(-self.x, -self.y)

