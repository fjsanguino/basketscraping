'''
import requests
from bs4 import BeautifulSoup

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=18&t=2017'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

select_jornadas_label = soup.find('select', {'name': 'jornadasDropDownList'})
for jornadas in select_jornadas_label.find_all('option'):
    print(jornadas['value'], jornadas.text)

form = soup.find_all("form", {"id": "Form1"})[0]
data = form.find_all("input")
params = {}
for d in data:
    params[d['name']] = d['value']

params['__EVENTTARGET'] = 'temporadasDropDownList'
params['__EVENTARGUMENT'] = ''
params['__LASTFOCUS'] = ''
params['lebOro'] = 'Estadisticas.aspx?g=1&t=0'
params['lf'] = 'Estadisticas.aspx?g=4&t=0'
params['lebPlata'] = 'Estadisticas.aspx?g=2&t=0'
params['lf2'] = 'Estadisticas.aspx?g=9&t=0'
params['eba'] = 'Estadisticas.aspx?g=27&t=0'
params['Circuito+Sub20'] = 'Resultados.aspx?g=11&t=0'
params['lebBronce'] = 'Estadisticas.aspx?g=15&t=2008'
params['temporadasDropDownList'] = '2017'
params['gruposDropDownList'] = ''
params['jornadasDropDownList'] = ''

r = requests.post(URL, data=params)
soup = BeautifulSoup(r.content, 'html.parser')

#p = '{'__EVENTARGUMENT': '', '__LASTFOCUS': '', 'lebOro': 'Estadisticas.aspx?g=1&t=0', 'lf': 'Estadisticas.aspx?g=4&t=0', 'lebPlata': 'Estadisticas.aspx?g=2&t=0', 'lf2': 'Estadisticas.aspx?g=9&t=0', 'eba': 'Estadisticas.aspx?g=27&t=0', 'Circuito+Sub20': 'Resultados.aspx?g=11&t=0', 'lebBronce': 'Estadisticas.aspx?g=15&t=2008', 'temporadasDropDownList': '2019', 'gruposDropDownList': '', 'jornadasDropDownList': '', '__VIEWSTATE': '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', '__VIEWSTATEGENERATOR': '141A904B', '__EVENTVALIDATION': '/wEdADh0vSZ5yS6N87MGvM9FSX4e0bh7k/WIjGHyxxr0UTpjvCz6cOz2ExR0hYK9zor+sBRlxy8rYX6qohgsLUJclYb8fSDI9u4MkLOaw3/vXr7+JYr8LFx70DQWN7dbV5Sm9OxEgettqSKkCBp1UoMoWOwFtU9Gk5GNV5fZII/0EvDMnR/kqSGF52FvZHDnfhB9ZWCi2WAda1CSbvdnEBwWF2+9sPU4sHI6/yrH98Y91pTj+FxAFvyUln5/9sZ09w1fX/6UKPVL9L47XIeF7pnykNnuNwJVaX0s3Mh/oUHC29I0D4DC8csm/jVps6oDYL3d8RdFuw4el3o0opfTOBHK+6y0vNqvTkj0Imsmgxqtg31X2lLu40qsE4N1k/7NegCqN07X+mfWbgGIQ/kIeJFev6HNQaiVSiGV0Em4iJrNTZ+g6xRqxTUMvfwxVMWWubmWcKop7yfcnXqN3BDL/pN62LuLeaOET8TDFXndeSaUYkU9ruuU+tI+Ua3Z/ylooyK1LRFMpcHXVQkSV5MqImD0ilPg1y2g20AXTWi8W7DUH7TwtXVz5wbOsZoEu+KLPKr/GnbQ766tieaR898ClH2GCAIydFv/gR2gZDs20UtP3FYGAcMTJbLZIBr1DZBUUx4cxnYV8owZzXWTYDGb86nYhPqLAPXwIaqrI2vY+6IR8I8MmgVZWAXlmxk4gVgO9XUPVBncbjbC8ghG+ZTN5rhzCo3glbASZXuCdU8lO/YeAXw5xx3yqvphHnpj6O4rPhXvMc4r84qLR9Tr/AYDjRu9P0O7ExhSbqybHMatXYN4xw2BIzbk+nsssByzMU0M4hJo6V+iiVYyXqv0qcNRxTPuybpI4Xxk+IOhoXTw/DQVRlvgfuV1noY15GpYRg6IJ2HTzkxJOiRCbc5k+aIz0ZQ65WBgN00JZsJtCoV8Xn5EQt5iMUy63rTfGvUWvXM6QvONzrAJ80euoqa8rapuCdoRVjBTU+J4WL4/B1NzVlCW1ucJjavtbxS9YIIPHBCrFJq+IHkoU6OliqfTdfvBDTMuk3x4luZBHd3RG2MJV8yTbqHj0Xmj3NkWAVwuFrgz+z+2+cHf2iBquuXUqJ73sh3k6Omb7Mg9KyHD9sjrBVPgfM9mFxZ8GlKVfqlHnkKYyzPFLPDbfGMIxOxQ4mV1/7OI3yJ58VOlL2P1XZpI/h97/YCLjiTYrr0olQpSMFAjxauDh94EpnaMDNJwA6s6wjeqsYpp', '__EVENTTARGET': 'temporadasDropDownList'}'
#p2 = '{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', '__VIEWSTATEGENERATOR': '141A904B', '__EVENTVALIDATION': '/wEdADh0vSZ5yS6N87MGvM9FSX4e0bh7k/WIjGHyxxr0UTpjvCz6cOz2ExR0hYK9zor+sBRlxy8rYX6qohgsLUJclYb8fSDI9u4MkLOaw3/vXr7+JYr8LFx70DQWN7dbV5Sm9OxEgettqSKkCBp1UoMoWOwFtU9Gk5GNV5fZII/0EvDMnR/kqSGF52FvZHDnfhB9ZWCi2WAda1CSbvdnEBwWF2+9sPU4sHI6/yrH98Y91pTj+FxAFvyUln5/9sZ09w1fX/6UKPVL9L47XIeF7pnykNnuNwJVaX0s3Mh/oUHC29I0D4DC8csm/jVps6oDYL3d8RdFuw4el3o0opfTOBHK+6y0vNqvTkj0Imsmgxqtg31X2lLu40qsE4N1k/7NegCqN07X+mfWbgGIQ/kIeJFev6HNQaiVSiGV0Em4iJrNTZ+g6xRqxTUMvfwxVMWWubmWcKop7yfcnXqN3BDL/pN62LuLeaOET8TDFXndeSaUYkU9ruuU+tI+Ua3Z/ylooyK1LRFMpcHXVQkSV5MqImD0ilPg1y2g20AXTWi8W7DUH7TwtXVz5wbOsZoEu+KLPKr/GnbQ766tieaR898ClH2GCAIydFv/gR2gZDs20UtP3FYGAcMTJbLZIBr1DZBUUx4cxnYV8owZzXWTYDGb86nYhPqLAPXwIaqrI2vY+6IR8I8MmgVZWAXlmxk4gVgO9XUPVBncbjbC8ghG+ZTN5rhzCo3glbASZXuCdU8lO/YeAXw5xx3yqvphHnpj6O4rPhXvMc4r84qLR9Tr/AYDjRu9P0O7ExhSbqybHMatXYN4xw2BIzbk+nsssByzMU0M4hJo6V+iiVYyXqv0qcNRxTPuybpI4Xxk+IOhoXTw/DQVRlvgfuV1noY15GpYRg6IJ2HTzkxJOiRCbc5k+aIz0ZQ65WBgN00JZsJtCoV8Xn5EQt5iMUy63rTfGvUWvXM6QvONzrAJ80euoqa8rapuCdoRVjBTU+J4WL4/B1NzVlCW1ucJjavtbxS9YIIPHBCrFJq+IHkoU6OliqfTdfvBDTMuk3x4luZBHd3RG2MJV8yTbqHj0Xmj3NkWAVwuFrgz+z+2+cHf2iBquuXUqJ73sh3k6Omb7Mg9KyHD9sjrBVPgfM9mFxZ8GlKVfqlHnkKYyzPFLPDbfGMIxOxQ4mV1/7OI3yJ58VOlL2P1XZpI/h97/YCLjiTYrr0olQpSMFAjxauDh94EpnaMDNJwA6s6wjeqsYpp', '__EVENTTARGET': 'temporadasDropDownList', '__EVENTARGUMENT': '', '__LASTFOCUS': '', 'lebOro': 'Estadisticas.aspx?g=1&t=0', 'lf': 'Estadisticas.aspx?g=4&t=0', 'lebPlata': 'Estadisticas.aspx?g=2&t=0', 'lf2': 'Estadisticas.aspx?g=9&t=0', 'eba': 'Estadisticas.aspx?g=27&t=0', 'Circuito+Sub20': 'Resultados.aspx?g=11&t=0', 'lebBronce': 'Estadisticas.aspx?g=15&t=2008', 'temporadasDropDownList': '2019', 'gruposDropDownList': '', 'jornadasDropDownList': ''}'
print('hello')
'''

import base
from stats import Stat
from games import Game
from jornadas import Jornada
from groups import Group
from seasons import Season
from leagues import League

import spacy
from spacy import displacy
import es_core_news_sm

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

nlp = es_core_news_sm.load()

engine = create_engine(open('database_info.txt', 'r').read())
base.Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

fh = open('../videos/out/Liga-LEB-ORO_2016-2017.txt')
for line in fh:
    page = requests.get(line[:-2])
    print(line[:-2])
    soup = BeautifulSoup(page.content, 'html.parser')

    info = soup.find('meta', {'name': 'description'})['content']
    #print(info)
    nlp_info = nlp(info)
    #print([(X.text, X.label_) for X in nlp_info.ents])




    title = soup.find('title').text
    #print(title)
    nlp_title = nlp(title)
    entities = [X.text for X in nlp_title.ents]
    #print([(X.text, X.label_) for X in nlp_title.ents])

    league = session.query(League).filter_by(name='LEB ORO').all()
    season = session.query(Season).filter_by(year = '2016/2017', league_id= league[0].id).all()

    query = session.query(Game, Group, Jornada).filter(Game.home_team.like('%' + entities[0] + '%'), Game.away_team.like('%' + entities[1] + '%'))\
        .filter(Group.season_id == season[0].id)\
        .filter(Group.id == Jornada.group_id)\
        .filter(Jornada.id == Game.jornada_id)

    output = query.all()

    if len(output) != 1:
        jornada_match = re.search(r'Jornada \d+', info, re.IGNORECASE)
        if (jornada_match):
            jornada = jornada_match.group()
            query = query.filter(Jornada.name.ilike('%' + jornada + '%'))
        output = query.all()
        if len(output) != 1:
            '''
            date_match = re.search(r'\d{4}-\d{2}-\d{2}', info)
            if (date_match):
                date = datetime.strptime(date_match.group(), '%Y-%m-%d').date()
                # print(date)
            '''
            date_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', info)
            if (date_match):
                date = datetime.strptime(date_match.group(), '%Y-%m-%d %H:%M')
                # print(date)

                query = query.filter(Game.date_played == date)
            output = query.all()
            if len(output) != 1:
                print('Problemitassssssssssssssssssssssssssssssssssssssssssssssssss')

fh.close()


print('finished')