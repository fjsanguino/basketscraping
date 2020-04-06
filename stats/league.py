import requests
from bs4 import BeautifulSoup

from DBInterface import checkLeagueStateInDB, insertLeagueInDB, checkSeasonStateInDB, insertSeasonInDB


def getLeagueURLsLeagueNamesFromMainURL(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    table_comp = soup.find("div", {"class": "navegarCompeticiones"})
    l = []
    for e in table_comp.find_all("a"):
        if 'resultados' in e['href'].lower():
            l.append('http://competiciones.feb.es/estadisticas/' + e['href'])
    leagues = []
    for e in table_comp.find_all("li", {"class": "competicion"}):
        if (int(e.text.find('[')) != -1):
            leagues.append(str(e.text[0:e.text.index('[')]))
        else:
            leagues.append(str(e.text))

    return l, leagues


def getSeasonsFromLeagueURL(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    temporadas = soup.find("select", {"id": "temporadasDropDownList"})
    t = []
    for e in temporadas.find_all('option'):
        t.append((e.text).replace('/', '-'))
    return t


def getGenderFromLeagueName(name):
    name = name.lower()
    if 'femenino' in name or 'femenina' in name:
        return 'female'
    elif 'masculino' in name or 'masculina' in name:
        return 'male'
    else:
        return 'male'


def getTypeFromLeagueName(name):
    posible_types = ['Mini', 'Amateur', 'Semiprofesional', 'Profesional']
    leagues = ['mini', 'infantil', 'cadete', 'sub', 'eba', 'liga femenina', 'leb']
    name = name.lower()
    if leagues[0] in name:
        return posible_types[0]
    elif leagues[1] in name or leagues[2] in name or leagues[3] in name:
        return posible_types[1]
    elif leagues[4] in name:
        return posible_types[2]
    elif leagues[5] in name or leagues[6] in name:
        return posible_types[3]
    else:
        return "None"

#also inserts seasons and leagues into database
def getLeaguesURLFromMainURL(URL):
    leagueURLs, leagueNames = getLeagueURLsLeagueNamesFromMainURL(URL)
    #print(leagueURLs[5])

    leagueids = []
    #for i in range(len(leagueURLs)):
    idx = [5,6,8,9,11]
    for i in idx:
        leagueName = leagueNames[i]
        type = getTypeFromLeagueName(leagueName)
        gender = getGenderFromLeagueName(leagueName)

        league_state = checkLeagueStateInDB(leagueName)

        if league_state[1] == 'finished':
            leagueURLs.remove(leagueURLs[i])
            break
        elif league_state[1] == 'processing':
            league_id = league_state[0]
        elif league_state[1] == 'not_inserted':
            league_id = insertLeagueInDB(leagueName, type, gender)
        else:  # error
            break
        leagueids.append(league_id)

    leagueURLs = leagueURLs[5:]
    leagueURLs.remove(leagueURLs[2])
    leagueURLs.remove(leagueURLs[4])
    leagueURLs = leagueURLs[:5]
    return leagueids, leagueURLs


if __name__ == '__main__':

    URL = 'http://competiciones.feb.es/estadisticas/default.aspx'

    print(getLeaguesURLFromMainURL(URL))

    exit(0)
