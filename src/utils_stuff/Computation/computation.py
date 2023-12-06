from utils_stuff.Position import Position
from utils_stuff.Computation.Linear import Linear
import math
import numpy as np

def abs_dist(position1 : Position, position2 : Position) -> float:
    return math.sqrt(np.abs(position2.x - position1.x)**2 + np.abs(position2.y - position1.y)**2)

def paralel(f1 : Linear, f2 : Linear):
    return f1.a == f2.a

def getCross(f1 : Linear, f2 : Linear) -> Position:
    assert not(paralel(f1, f2))
    x = (f1.b - f2.b)/(f2.a - f1.a)
    y = f1.f(x)
    return Position(x, y)

def centralSymmetry(coo : Position, center : Position):
    return Position(2*center.x - coo.x, 2*center.y - coo.y)