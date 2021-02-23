from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from base import Base
from sqlalchemy.orm import relationship


class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String(128))
    type = Column(String(64))
    gender = Column(String(16))

    is_statistics = Column(Boolean)
    state_statistics = Column(String(16)) #TODO: change for ENUM

    is_video = Column(Boolean)
    state_video = Column(String(16))

    is_actions = Column(Boolean)
    state_actions = Column(String(16))

    seasons = relationship("Season", back_populates = "league")

    def __init__(self, name, type, gender, is_statistics=None, state_statistics=None, is_video=None, state_video=None, is_actions=None, state_actions=None, seasons=[]):

        self.name = name
        self.type = type
        self.gender = gender

        self.is_statistics = is_statistics
        self.state_statistics = state_statistics

        self.is_video = is_video
        self.state_video = state_video

        self.is_actions = is_actions
        self.state_actions = state_actions

        self.seasons = seasons

    def __repr__(self):
        return f'Game({self.league_id}, {self.year})'
    def __str__(self):
        return str(self.id) + ', ' + str(self.league_id) + ', ' + str(self.year)

    @staticmethod
    def scrapSeasons_statsLEB(URL, league, session):
        import seasons
        import requests
        from bs4 import BeautifulSoup

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        params = {}

        params['__EVENTARGUMENT'] = ''
        params['__LASTFOCUS'] = ''
        params['lebOro'] = 'Estadisticas.aspx?g=1&t=0'
        params['lf'] = 'Estadisticas.aspx?g=4&t=0'
        params['lebPlata'] = 'Estadisticas.aspx?g=2&t=0'
        params['lf2'] = 'Estadisticas.aspx?g=9&t=0'
        params['eba'] = 'Estadisticas.aspx?g=27&t=0'
        params['Circuito+Sub20'] = 'Resultados.aspx?g=11&t=0'
        params['lebBronce'] = 'Estadisticas.aspx?g=15&t=2008'
        params['temporadasDropDownList'] = '2019'
        params['gruposDropDownList'] = ''
        params['jornadasDropDownList'] = ''

        form = soup.find_all("form", {"id": "aspnetForm"})[0]
        data = form.find_all("input")
        for d in data:
            params[d['name']] = d['value']

        league_db = session.query(League).filter_by(name=league.name).first()
        if league_db != None:
            if league_db.state_statistics == 'finished':
                return league_db.state_statistics


        select_seasons_label = soup.find('select', {'name': '_ctl0:MainContentPlaceHolderMaster:temporadasDropDownList'})

        allSeasons_finished = True
        for season in select_seasons_label.find_all('option'):
            print(season.text)


            not_repeat = True
            try:
                season['selected']
            except:
                not_repeat = False


            params['temporadasDropDownList'] = season['value']
            params['__EVENTTARGET'] = 'temporadasDropDownList'


            posible_seasons = ['2019', '2018', '2017', '2016']
            if season['value'] in posible_seasons:
                season_state = seasons.Season.scrapGroups_statsLEB(URL, params, season.text, league_db, session, not_repeat, soup)
                if season_state == 'processing':
                    allSeasons_finished = False

        if allSeasons_finished:
            league_db.state_statistics = 'finished'

        return league_db.state_statistics
