import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import mysql.connector
import os

import DBInterface



#import wget
import itertools

#En total hay 8907 videos en canalfeb.tv

#TODO: check if the year/competition is done

#TODO: check if the jornada is already done

def getLeaguesFromMainPage(URL):
    page = requests.get(URL)

    '''Parses the recieved information (HTML in this case) to BeautifulSoup'''
    soup = BeautifulSoup(page.content, 'html.parser')

    competitions = soup.find("li", {"class":"uk-parent"})
    #print(competitions.prettify())

    links = competitions.find_all('a')
    #print(links)

    '''Gets all the links to the statistics of each game'''
    l = []
    for link in links:

        '''Restringe las ligas'''
        if link['href'] in ['/competiciones-mobile/seleccion', '/competiciones-mobile/cto-espana-ssaa', '/competiciones-mobile/cto-espana-clubes-junior-femenino', '/competiciones-mobile/cto-espana-clubes-junior-masculino', '/competiciones-mobile/cto-espana-clubes-cadete-femenino', '/competiciones-mobile/cto-espana-clubes-cadete-masculino', '/competiciones-mobile/cto-espana-clubes-infantil-femenino', '/competiciones-mobile/cto-espana-clubes-infantil-masculino']:
            continue

        l.append(URL + link['href'])


        page = requests.get(URL + link['href'])
        soup = BeautifulSoup(page.content, 'html.parser')

        competitions = soup.find("div", {"class": "nav-ligas"})
        if competitions:
            more_links = competitions.find_all('a')
            for m_l in more_links:
                l.append(URL + m_l['href'])

    return l

#def getLeaguesFromDataBase():

def getGameURLFromSeason(URL):

    '''Gets all the links to all the pages'''
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    league_name = soup.find("title").string
    season = soup.find("h1", {"class": "n3-channel-header"}).string
    season = '20' + season[season.find('-')-2:season.find('-')] + '-20' + season[season.find('-')+1:season.find('-')+3]
    #print(liga_name, season)
    #print(season)

    #season_ids = DBInterface.getSeasonID(liga_name, season)
    #print(season_ids)
    #season_id = input(which is the one)

    paginations = soup.find("ul", {"class": "uk-pagination"})
    if paginations:
        links = paginations.find_all('a')

        final_page = links[-1]['href'][links[-1]['href'].rfind('p=')+2:]

        GameURLs = []
        for i in range(1,int(final_page)+1):
            page = requests.get(URL, params={'p':str(i)})
            soup = BeautifulSoup(page.content, 'html.parser')
            games = soup.find_all("p", {"class": "video-title"})
            for g in games:
                GameURLs.append(g.a['href'])
    else:
        GameURLs = []
        soup = BeautifulSoup(page.content, 'html.parser')
        games = soup.find_all("p", {"class": "video-title"})
        for g in games:
            GameURLs.append(g.a['href'])

    return GameURLs, league_name, season

URL = 'https://canalfeb.tv/video/?videoId=e-11790'
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



    scripts = soup.find_all('script')

    for i in range(len(scripts)):
        if i != len(scripts)-2:
            pass
        else:
            url_script = str(scripts[i].prettify())
            begin_index =url_script.find("http")
            end_index = url_script.find(";")-1
            url_info = url_script[begin_index:end_index]

    '''Cojo la información de la url que gestiona el video'''
    video_info = requests.get(url_info)
    video_info = str(video_info.content)
    video_info = video_info[2:video_info.find("embeddable")-2] +'}]}' #me quedo solo con parte del json porque da fallo si no
    #print(video_info)
    video_info = json.loads(video_info)

    download_url = video_info['videos'][0]['downloadURL']

    if download_url[-4:] == '.mp4':
        print(download_url)
    return download_url, game_id

    #wget.download(download_url, '/home/fjsanguino/Downloads/partido.mp4')

    #query = 'select id from leagues where name={} and season={}'.format(league[name], league[season])
    #query2 = 'select state from games where league_id = {} and jornada = {} and home_team = {} and away_team = {}'.format(query_result, game['jornada'], game['home_team'], game['away_team'])

    #query_update = 'update video_state...'
    #query_update_league = 'update video_state...'

if __name__ == '__main__':
    #URL = 'https://canalfeb.tv/video/?videoId=e-11790'
    #getVideoFromGameURL(URL)
    #exit(0)
    connection = mysql.connector.connect(
        host="remotemysql.com",
        user="g3GJdRGWE4",
        passwd="4I1ZMfcMXg",
        database="g3GJdRGWE4"
    )


    '''
    if (not os.path.exists('out')):
        os.makedirs('out')


    # Init DB

    URL = 'https://canalfeb.tv'
    print('starting')

    competitions = getLeaguesFromMainPage(URL)
    print(competitions)
    total_count = 0
    for c in competitions:
        #print(c)
        count = 0
        gamesURL, league_name, season = getGameURLFromSeason(c)
        file_name = 'out/' + league_name.replace(" ", "-") + '_' + season + '.txt'
        for g in gamesURL:
            #print(g, end='\r')
            #print(g)
            with open(file_name, "a") as file_object:
                file_object.write(g + '\n')
            count += 1
        total_count += count

        print(c, count, total_count)

    exit(0)
    '''
    file_name = 'out/Liga-LEB-ORO_2019-2020'
    file_name_read = file_name + '.txt'
    season_id = 103

    f = open(file_name_read, "r")
    not_done = []
    not_more = False
    for g in f:
        g = g[:-2]
        if not_more:
            not_done.append(g)
        else:
            download_url, game_id = getVideoFromGameURL(g, season_id)
            if download_url == None and game_id == None:
                not_done.append(g)
                continue
            if download_url == -1 and game_id == -1:
                not_more = True
                continue
            DBInterface.updateGame(download_url, game_id)

    file_name_write = file_name + '_1.txt'
    with open(file_name_write, "a") as file_object:
        for g in not_done:
            file_object.write(g + '\n')




