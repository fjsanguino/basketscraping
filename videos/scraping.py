import requests
from bs4 import BeautifulSoup
import json
import wget
import itertools

#En total hay 8907 videos en canalfeb.tv

#TODO: check if the year/competition is done

#TODO: check if the jornada is already done

URL = 'https://canalfeb.tv'
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

URL = 'https://canalfeb.tv/competiciones/liga-leb-oro'
def getGameURLFromLeagues(URL):

    '''Gets all the links to all the pages'''
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
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

    return GameURLs

URL = 'https://canalfeb.tv/video/?videoId=e-11790'
def getVideoFromGameURL(URL):
    page = requests.get(URL)

    '''Parses the recieved information (HTML in this case) to BeautifulSoup'''
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())

    info = soup.find('meta', {'name': 'twitter:title'})
    moreInfo = soup.find('meta', {'name': 'twitter:description'})
    print(info.attrs['content'], moreInfo)
    info = info['content'].split(' VS ')
    moreInfo = moreInfo['content'].split(' / ')

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

    #info = video_info['videos'][0]['title'].split(' VS ')
    #moreInfo = video_info['videos'][0]['description'].split('\\/')

    league = {'name': moreInfo[1],
              'season': moreInfo[2]}
    game = {'home_team': info[0],
            'away_team': info[1],
            'jornada': moreInfo[0]}
    #print(league, game)

    download_url = video_info['videos'][0]['downloadURL']

    if download_url[-4:] == '.mp4':
        print(download_url)
    return download_url

    #wget.download(download_url, '/home/fjsanguino/Downloads/partido.mp4')

    #query = 'select id from leagues where name={} and season={}'.format(league[name], league[season])
    #query2 = 'select state from games where league_id = {} and jornada = {} and home_team = {} and away_team = {}'.format(query_result, game['jornada'], game['home_team'], game['away_team'])

    #query_update = 'update video_state...'
    #query_update_league = 'update video_state...'

if __name__ == '__main__':
    #URL = 'https://canalfeb.tv/video/?videoId=e-11790'
    #getVideoFromGameURL(URL)
    #exit(0)
    URL = 'https://canalfeb.tv'
    print('starting')
    competitions = getLeaguesFromMainPage(URL)
    print(competitions)
    total_count = 0
    for c in competitions:
        #print(c)
        count = 0
        gamesURL = getGameURLFromLeagues(c)
        for g in gamesURL:
            print(g, end='\r')
            count += 1
        total_count += count
        print(c, count, total_count)
            #getVideoFromGameURL(g)
