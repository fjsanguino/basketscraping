from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship

import requests
from bs4 import BeautifulSoup

from base import Base



class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement = True)
    jornada_id = Column(Integer, ForeignKey("jornadas.id"), nullable=False)
    jornada = relationship("Jornada", back_populates="games")

    home_team = Column(String(64))
    away_team = Column(String(64))
    result = Column(String(16))
    date_played = Column(DateTime)

    referee_1 = Column(String(512))
    referee_2 = Column(String(512))
    referee_3 = Column(String(512))

    place = Column(String(128))
    court = Column(String(128))

    score_q1 = Column(String(16))
    score_q2 = Column(String(16))
    score_q3 = Column(String(16))
    score_q4 = Column(String(16))

    played = Column(Boolean)

    is_statistics = Column(Boolean)
    state_statistics = Column(String(16)) #TODO: change for ENUM

    is_video = Column(Boolean)
    state_video = Column(String(16))

    is_actions = Column(Boolean)
    state_actions = Column(String(16))

    stats = relationship("Stat", back_populates="game")

    def __init__(self, home_team, away_team, result, date_played, referee_1, referee_2, referee_3, place, court, score_q1, score_q2, score_q3, score_q4, played=None, is_statistics=None, state_statistics=None, is_video=None, state_video=None, is_actions=None, state_actions=None, stats=[]):

        self.home_team = home_team
        self.away_team = away_team
        self.result = result
        self.date_played = date_played

        self.referee_1 = referee_1
        self.referee_2 = referee_2
        self.referee_3 = referee_3

        self.place = place
        self.court = court

        self.score_q1 = score_q1
        self.score_q2 = score_q2
        self.score_q3 = score_q3
        self.score_q4 = score_q4

        self.played = played

        self.is_statistics = is_statistics
        self.state_statistics = state_statistics

        self.is_video = is_video
        self.state_video = state_video

        self.is_actions = is_actions
        self.state_actions = state_actions

        self.stats = stats

    def __repr__(self):
        return f'Game({self.home_team}, {self.away_team})'
    def __str__(self):
        return str(self.id) + ', ' + str(self.jornada_id) + ', ' + str(self.home_team) + ', ' + str(self.away_team) + ', ' + str(self.result) + ', ' + str(self.date_played)

    @staticmethod
    def scrapStats_statsLEB(gameURL, finished_game, jornada, session):
        from stats import Stat
        from games_utils import getGameDataFromGameURL
        from datetime import datetime

        page = requests.get(gameURL)  # Sends a GET HTTP request
        soup = BeautifulSoup(page.content, 'html.parser')  # Parses the content using a HTML canvas

        game = getGameDataFromGameURL(soup)
        game.jornada = jornada

        game.played = True
        if not(finished_game):
            game.played = False
            if datetime.now() > game.date_played:
                game.is_statistics = False
                game.state_statistics = 'finished'
                return 'finished'
            else:
                return 'processing'


        #check if game in database
        game_db = session.query(Game).filter_by(home_team=game.home_team, away_team=game.away_team, result=game.result,
                           date_played=game.date_played, jornada_id = jornada.id).first()


        if game_db.state_statistics == 'processing':
            for st in session.query(Stat).filter_by(game_id=game_db.id).all():
                session.delete(st)
        elif game_db.state_statistics == 'finished':
            return game_db.state_statistics

        print(gameURL)

        ####Iterates over the tables found that have stats
        table = soup.find("table", {"class": "tablaDataGrid"})

        counttables = 0
        team = game_db.home_team
        while table != None:
            counttables = counttables + 1

            ######Gets all the data
            a = table.tr
            a = a.next_sibling  # Needed beacuse the first <tr> is an empty string
            while a.next_sibling.next_sibling != None:
                b = a.td
                ###Variable defition
                stat = Stat()
                stat.team = team
                for i in range(18):
                    if i == 0:  # Titular o no
                        tit = False
                        if b.string == None:
                            tit = True
                        # print('Titular:', tit)
                        stat.starter = tit
                    if i == 1:  # Numero de jugador
                        # print('Num jug:', b.span.string)
                        stat.number = b.span.string
                    if i == 2:  # Nombre jugador
                        # print('nombre:', b.a.string)
                        stat.player = b.a.string
                    if i == 3:  # Minutos jugados
                        # print('Min:', b.span.string)
                        stat.MIN = b.span.string
                    if i == 4:  # Puntos anotados
                        # print('Puntos:', b.span.string)
                        stat.PTS = b.span.string
                    if i == 5:  # 2pts(anotados/intentados) porcentaje%
                        # print('2pts:', b.span.string)
                        zone = b.span.string
                        stat._2PM = zone[zone.find('/') - 1]
                        stat._2PA = zone[zone.find('/') + 1]
                    if i == 6:  # 3pts(anotados/intentados) porcentaje%
                        # print('3pts:', b.span.string)
                        trip = b.span.string
                        stat._3PM = trip[trip.find('/') - 1]
                        stat._3PA = trip[trip.find('/') + 1]
                    if i == 7:  # Tiros campo(anotados/intentados) porcentaje%
                        hola = 1
                        # print('Campo:', b.span.string)
                    if i == 8:  # T.L.(anotados/intentados) porcentaje%
                        # print('T.L:', b.span.string)
                        free = b.span.string
                        stat.FTM = free[free.find('/') - 1]
                        stat.FTA = free[free.find('/') + 1]
                    if i == 9:  # Rebotes, def of to
                        c = b.td
                        # print(b)
                        reb = []
                        count = 0
                        while c.next_sibling != None:
                            count = count + 1
                            if count % 2 == 1:  # I dont know why but the odd children are empty strings
                                reb.append(c.span.string)
                            c = c.next_sibling
                        # print('Reb: ', reb)
                        stat.DREB = reb[0]
                        stat.OREB = reb[1]
                    if i == 10:  # Asistencias
                        # print('As:', b.span.string)
                        stat.AST = b.span.string
                    if i == 11:  # Balones recuperados
                        # print('Recuperados:', b.span.string)
                        stat.STL = b.span.string
                    if i == 12:  # Balones perdidos
                        # print('perdidos:', b.span.string)
                        stat.TOV = b.span.string
                    if i == 13:  # Tapones, favor contra
                        c = b.td
                        tap = []
                        count = 0
                        while c.next_sibling != None:
                            count = count + 1
                            if count % 2 == 1:
                                tap.append(c.span.string)
                            c = c.next_sibling
                        # print('Tap:', tap)
                        stat.BLKM = tap[0]
                        stat.BLKR = tap[1]
                    if i == 14:  # Mates
                        # print('Mates:', b.span.string)
                        stat.DNK = b.span.string
                    if i == 15:  # Faltas, cometidas recibidas
                        c = b.td
                        fal = []
                        count = 0
                        while c.next_sibling != None:
                            count = count + 1
                            if count % 2 == 1:  # I dont know why but the odd children are empty strings
                                fal.append(c.span.string)
                            # print(c)
                            c = c.next_sibling
                        # print('fouls', fal)
                        stat.PFM = fal[0]
                        stat.PFR = fal[1]
                    if i == 16:  # Valoracion
                        # print('Valoracion:', b.span.string)
                        stat.VAL = b.span.string
                    if i == 17:  # +/-
                        # print('+/-:', b.span.string)
                        stat.PM = b.span.string
                    b = b.next_sibling

                ##Inserts Data in Database
                stat.game = game_db
                session.add(stat)

                a = a.next_sibling

            ###Find the next table to get the stat
            table = table.findNext("table", {"class": "tablaDataGrid"})
            team = game_db.away_team

        game.state_statistics = 'finished'

        return game_db.state_statistics

