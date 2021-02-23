from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from base import Base
from sqlalchemy.orm import relationship

class Stat(Base):
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True, autoincrement = True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship("Game", back_populates="stats")

    team = Column(String(64))
    player = Column(String(128))

    number = Column(Integer)
    starter = Column(Boolean)
    MIN = Column(String(8))
    PTS = Column(Integer)

    _2PA = Column('2PA', Integer)
    _2PM = Column('2PM', Integer)
    _3PA = Column('3PA', Integer)
    _3PM = Column('3PM', Integer)

    FTA = Column(Integer)
    FTM = Column(Integer)
    DREB = Column(Integer)
    OREB = Column(Integer)

    AST = Column(Integer)
    STL = Column(Integer)
    TOV = Column(Integer)
    BLKM = Column(Integer)

    BLKR = Column(Integer)
    DNK = Column(Integer)
    PFR = Column(Integer)

    PFM = Column(Integer)
    VAL = Column(Integer)
    PM = Column(Integer)

    '''
    def __init__(self, player, number, starter, MIN, PTS, _2PA, _2PM, _3PA, _3PM, FTA, FTM, DREB, OREB, AST, STL, TOV, BLKM, BLKR, DNK, PFR, PFM, VAL, PM):

        self.player = player
        self.number = number
        self.starter = starter

        self.MIN = MIN
        self.PTS = PTS
        self._2PA = _2PA
        self._2PM = _2PM
        self._3PA = _3PA

        self._3PM = _3PM
        self.FTA = FTA
        self.FTM = FTM
        self.DREB = DREB

        self.OREB = OREB
        self.AST = AST
        self.STL = STL
        self.TOV = TOV

        self.BLKM = BLKM
        self.BLKR = BLKR
        self.DNK = DNK
        self.PFR = PFR

        self.PFM = PFM
        self.VAL = VAL
        self.PM = PM
    '''
    def __repr__(self):
        return f'Stat({self.game_id}, {self.player})'
    def __str__(self):
        return str(self.id) + ', ' + str(self.game_id) + ', ' + str(self.player)

    @staticmethod
    def getSomething():
        print('Llegué aquí')
