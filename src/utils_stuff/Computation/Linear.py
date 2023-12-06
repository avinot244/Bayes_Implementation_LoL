from utils_stuff.Position import Position
class Linear:
    def __init__(self,
                 coo1 : Position = None,
                 coo2 : Position = None,
                 a : int = None,
                 b : int = None) -> None:
        if coo1 == None and coo2 == None:
            assert a != None and b != None
            self.a = a
            self.b = b
        elif a == None and b == None:
            assert coo1 != None and coo2 != None
            if coo1.x == coo2.x:
                self.a = (coo2.y - coo1.y)/(coo2.x+1 - coo1.x)
            else:
                self.a = (coo2.y - coo1.y)/(coo2.x - coo1.x)
            self.b = coo1.y - self.a * coo1.x
    
    def f(self, x):
        return self.a * x + self.b
    
    def __str__(self) -> str:
        return "(a: {}, b: {})".format(self.a, self.b)