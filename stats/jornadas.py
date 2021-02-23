from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from base import Base
from sqlalchemy.orm import relationship


class Jornada(Base):
    __tablename__ = 'jornadas'

    id = Column(Integer, primary_key=True, autoincrement = True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship("Group", back_populates = "jornadas")
    name = Column(String(64))

    is_statistics = Column(Boolean)
    state_statistics = Column(String(16)) #TODO: change for ENUM

    is_video = Column(Boolean)
    state_video = Column(String(16))

    is_actions = Column(Boolean)
    state_actions = Column(String(16))

    games = relationship("Game", back_populates="jornada")

    def __init__(self, name, is_statistics=None, state_statistics=None, is_video=None, state_video=None, is_actions=None, state_actions=None, games=[]):

        self.name = name

        self.is_statistics = is_statistics
        self.state_statistics = state_statistics

        self.is_video = is_video
        self.state_video = state_video

        self.is_actions = is_actions
        self.state_actions = state_actions

        self.games = games

    def __repr__(self):
        return f'Game({self.league_id}, {self.year})'
    def __str__(self):
        return str(self.id) + ', ' + str(self.league_id) + ', ' + str(self.year)

    @staticmethod
    def scrapGames_statsLEB(URL, jornada_params, jornada_name, group, session, only_oneJornada, last_soup):
        import games
        import requests
        from bs4 import BeautifulSoup
        import re
        #requests post
        page = requests.post(URL, data=jornada_params)
        soup = BeautifulSoup(page.content, 'html.parser')

        if only_oneJornada:
            soup = last_soup

        form = soup.find_all("form", {"id": "Form1"})[0]
        data = form.find_all("input")
        for d in data:
            jornada_params[d['name']] = d['value']

        results = soup.find("div", {"class": "contentTablaDataGrid"})

        #Build Jornada
        jornada = Jornada(jornada_name, True, 'processing')
        jornada.group = group

        jornada_db = session.query(Jornada).filter_by(name=jornada.name, group_id=group.id).first()

        if jornada_db.state_statistics == 'finished':
            return jornada_db.state_statistics

        partial_gameURLs = results.table.find_all('a')

        allGames_finished = True
        for link in partial_gameURLs:
            if not (link['href'].find('Partido')):
                gameURL = 'http://competiciones.feb.es/estadisticas/' + link['href']
                if link.string == '*-*':
                    finished_game = False
                else:
                    finished_game = True

                game_state = games.Game.scrapStats_statsLEB(gameURL, finished_game, jornada_db, session)
                if game_state == 'processing':
                    allGames_finished = False

        if allGames_finished:
            jornada_db.state_statistics = 'finished'

        session.commit()
        return jornada_db.state_statistics