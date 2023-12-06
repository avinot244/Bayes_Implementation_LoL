from utils_stuff.Position import Position

class Zone:
    def __init__(self,
                 boundary : list[Position]) -> None:
        
        self.boundary = boundary