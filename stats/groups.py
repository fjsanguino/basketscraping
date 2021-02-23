from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from base import Base
from sqlalchemy.orm import relationship

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement = True)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    season = relationship("Season", back_populates = "groups")
    group_name = Column(String(32))

    is_statistics = Column(Boolean)
    state_statistics = Column(String(16)) #TODO: change for ENUM

    is_video = Column(Boolean)
    state_video = Column(String(16))

    is_actions = Column(Boolean)
    state_actions = Column(String(16))

    jornadas = relationship("Jornada", back_populates="group")

    def __init__(self, group_name, is_statistics=None, state_statistics=None, is_video=None, state_video=None, is_actions=None, state_actions=None, jornadas=[]):

        self.group_name = group_name

        self.is_statistics = is_statistics
        self.state_statistics = state_statistics

        self.is_video = is_video
        self.state_video = state_video

        self.is_actions = is_actions
        self.state_actions = state_actions

        self.jornadas = jornadas

    def __repr__(self):
        return f'Game({self.season_id}, {self.group_name})'
    def __str__(self):
        return str(self.id) + ', ' + str(self.season_id) + ', ' + str(self.group_name)

    @staticmethod
    def scrapJornadas_statsLEB(URL, params, group_name, season, session, not_repeat, last_soup):
        import jornadas
        import requests
        from bs4 import BeautifulSoup

        page = requests.post(URL, data=params)
        soup = BeautifulSoup(page.content, 'html.parser')

        if not_repeat:
            soup = last_soup

        form = soup.find_all("form", {"id": "Form1"})[0]
        data = form.find_all("input")
        for d in data:
            params[d['name']] = d['value']

        group = Group(group_name, True, 'processing')
        group.season = season

        group_db = session.query(Group).filter_by(group_name=group.group_name, season_id=season.id).first()

        if group_db.state_statistics == 'finished':
            return group_db.state_statistics

        allJornadas_finished = True

        select_jornadas_label = soup.find('select', {'name': 'jornadasDropDownList'})
        for jornada in select_jornadas_label.find_all('option'):
            print(jornada.text)

            not_repeat = True
            try:
                jornada['selected']
            except:
                not_repeat = False

            params['jornadasDropDownList'] = jornada['value']
            params['__EVENTTARGET'] = 'jornadasDropDownList'
            jornada_state = jornadas.Jornada.scrapGames_statsLEB(URL, params, jornada.text, group_db, session, not_repeat, soup)
            if jornada_state == 'processing':
                allJornadas_finished = False

        if allJornadas_finished:
            group_db.state_statistics = 'finished'


        return group_db.state_statistics