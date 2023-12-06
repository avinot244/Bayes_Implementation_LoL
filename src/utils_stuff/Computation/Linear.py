class Linear:
    def __init__(self,
                 a : int,
                 b : int) -> None:
        self.a = a
        self.b = b
    
    def f(self, x):
        return self.a * x + self.b
    