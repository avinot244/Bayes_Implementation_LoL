class TimeParser:
    def __init__(self, min:int=0, sec:int=0):
        self.min = min
        self.sec = sec
    
    def convert_raw(self, time:int):
        assert time//1000 > 0
        self.min = time//100
        self.sec = time%100
    
    def convert_to_sec(self):
        return self.sec + 60*self.min

    def sec_to_minsec(time):
        res = TimeParser()
        if time > 60:
            res.min = time//60
            res.sec = time%60
        else:
            res.sec = time
        return res
