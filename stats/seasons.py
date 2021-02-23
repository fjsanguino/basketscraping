from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from base import Base
from sqlalchemy.orm import relationship

class Season(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True, autoincrement = True)
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False)
    league = relationship("League", back_populates = "seasons")
    year = Column(String(16))

    is_statistics = Column(Boolean)
    state_statistics = Column(String(16)) #TODO: change for ENUM

    is_video = Column(Boolean)
    state_video = Column(String(16))

    is_actions = Column(Boolean)
    state_actions = Column(String(16))

    groups = relationship("Group", back_populates="season")

    def __init__(self, year, is_statistics=None, state_statistics=None, is_video=None, state_video=None, is_actions=None, state_actions=None, groups = []):

        self.year = year

        self.is_statistics = is_statistics
        self.state_statistics = state_statistics

        self.is_video = is_video
        self.state_video = state_video

        self.is_actions = is_actions
        self.state_actions = state_actions

        self.groups = groups

    def __repr__(self):
        return f'Game({self.league_id}, {self.year})'
    def __str__(self):
        return str(self.id) + ', ' + str(self.league_id) + ', ' + str(self.year)

    @staticmethod
    def scrapGroups_statsLEB(URL, params, year, league, session, not_repeat, last_soup):
        import groups
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

        season = Season(year, True, 'processing')
        season.league = league

        season_db = session.query(Season).filter_by(year=season.year, league_id=league.id).first()

        if season_db.state_statistics == 'finished':
            return season_db.state_statistics


        select_groups_label = soup.find('select', {'name': 'gruposDropDownList'})

        allGroups_finished = True
        for group in select_groups_label.find_all('option'):
            print(group.text)

            not_repeat = True
            try:
                group['selected']
            except:
                not_repeat = False

            params['gruposDropDownList'] = group['value']
            params['__EVENTTARGET'] = 'gruposDropDownList'
            group_state = groups.Group.scrapJornadas_statsLEB(URL, params, group.text, season_db, session, not_repeat, soup)
            if group_state == 'processing':
                allGroups_finished = False

        if allGroups_finished:
            season_db.state_statistics = 'finished'

        return season_db.state_statistics