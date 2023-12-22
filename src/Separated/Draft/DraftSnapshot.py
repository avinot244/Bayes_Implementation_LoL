from Separated.Draft.Team import Team

class DraftSnapshot:
    def __init__(self,
                 seqIdx : int,
                 filename : str,
                 teamOne : Team,
                 teamTwo : Team
                 ) -> None:
        self.seqIdx = seqIdx
        self.filename = filename
        self.teamOne = teamOne
        self.teamTwo = teamTwo