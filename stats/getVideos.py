from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests
from bs4 import BeautifulSoup

import base

engine = create_engine(open('stats/database_info.txt', 'r').read())
base.Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def getVideoFromGameURL(URL, season_id):
    page = requests.get(URL)

    '''Parses the recieved information (HTML in this case) to BeautifulSoup'''
    soup = BeautifulSoup(page.content, 'html.parser')

    # info = video_info['videos'][0]['title'].split(' VS ')
    # moreInfo = video_info['videos'][0]['description'].split('\\/')

    info = soup.find('meta', {'name': 'twitter:title'})
    moreInfo = soup.find('meta', {'name': 'twitter:description'})

    # info = info['content'].split(' VS ')
    # moreInfo = moreInfo['content'].split(' / ')
    '''
    league = {'name': moreInfo[1],
              'season': moreInfo[2]}
    game = {'home_team': info[0],
            'away_team': info[1],
            'jornada': moreInfo[0]}
    '''

    print(info['content'], '|||', moreInfo['content'])

    columns = []
    values = []
    while True:
        column = input('which info do you want to query:')
        if column == '0':
            break
        columns.append(column)
        values.append(input('With which value:'))

    query = "select group_name, jornada, games.* from games, jornadas, `groups` where games.jornada_id = jornadas.id and jornadas.group_id = `groups`.id and  `groups`.season_id = {}".format(
        season_id)
    for i in range(len(columns)):
        if i != len(columns) - 1:
            query += columns[i] + "=" + values[i] + " and "
        else:
            query += columns[i] + "=" + values[i]

    df = pd.read_sql(query, con=connection)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

    game_id = input('which game_id has?')

    if game_id == '0':
        return None, None

    if game_id == '-1':
        return -1, -1

URL = 'https://canalfeb.tv/video/?videoId=e-11790'


