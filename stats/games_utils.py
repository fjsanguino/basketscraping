from datetime import datetime
from games import Game

'''Sends a GET HTTP request to the given URL'''
# PARTIDO DE EJEMPLO


def getDate(soup):
    # dia, mes, año
    dia = [int(e) for e in soup.find("span", {"id": "fechaLabel"}).text.split('/')]
    # hora, min
    hora = [int(e) for e in soup.find("span", {"id": "horaLabel"}).text.split(':')]
    # datetime(year, month, day, hour, minute, second, microsecond)
    fecha = datetime(dia[2], dia[1], dia[0], hora[0], hora[1])
    return fecha

def getReferees(soup):
    if soup.find("span", {"id": "arbitroPrincipalLabel"}).string:
        arbitroP = str(soup.find("span", {"id": "arbitroPrincipalLabel"}).text)
        arbitroP = arbitroP[0:arbitroP.index(',')]
    else:
        arbitroP = None
    if soup.find("span", {"id": "arbitroAuxiliarLabel"}).string:
        arbitroA1 = str(soup.find("span", {"id": "arbitroAuxiliarLabel"}).text)
        arbitroA1 = arbitroA1[0:arbitroA1.index(',')]
    else:
        arbitroA1 = None
    if soup.find("span", {"id": "arbitroAuxiliar2Label"}).text:
        arbitroA2 = str(soup.find("span", {"id": "arbitroAuxiliar2Label"}).string)
        arbitroA2 = arbitroA2[0:arbitroA2.index(',')]
    else:
        arbitroA2 = None

    arbitros = [arbitroP, arbitroA1, arbitroA2]

    return arbitros

def getTeams(soup):
    home_team = soup.find("td", {"class": "equipoLocal"}).text
    away_team = soup.find("td", {"class": "equipoVisitante"}).text
    print(home_team, away_team)
    return home_team, away_team

def getResult(soup):
    table_cuartos = soup.find("table", {"class": "tablaResultadosCuartos"})
    if not(soup.find("table", {"class": "tablaResultadosCuartos"})):
        return None, None
    pts_eq1 = [int(e.text) for e in table_cuartos.find_all('span')[1:5]]
    pts_eq2 = [int(e.text) for e in table_cuartos.find_all('span')[6:10]]
    return pts_eq1, pts_eq2

def getScores(soup):
    
    resultLocal = int(soup.find("span", {"id": "resultadoLocalLabel"}).text)
    resultVisitante = int(soup.find("span", {"id": "resultadoVisitanteLabel"}).text)
    # resultado como lista de enteros
    result2 = [int(soup.find("span", {"id": "resultadoLocalLabel"}).text), int(soup.find("span", {"id": "resultadoVisitanteLabel"}).text)]
    # resultado como concatenacion de strings
    result = str(resultLocal) + ' - ' + str(resultVisitante)
    return result

def getLocation(soup):
    court = str(soup.find("span", {"id": "pistaJuegoLabel"}).text)
    city = str(soup.find("span", {"id": "localidadLabel"}).text)
    region = str(soup.find("span", {"id": "provinciaLabel"}).text)
    return court, city, region

def getGameDataFromGameURL(soup):

    date_played = getDate(soup)

    referee_1, referee_2, referee_3 = getReferees(soup)

    pts_eq1, pts_eq2 = getResult(soup)

    if pts_eq1 != None and pts_eq2 != None:
        score_q1 = str(pts_eq1[0]) + ' - ' + str(pts_eq2[0])
        score_q2 = str(pts_eq1[1]) + ' - ' + str(pts_eq2[1])
        score_q3 = str(pts_eq1[2]) + ' - ' + str(pts_eq2[2])
        score_q4 = str(pts_eq1[3]) + ' - ' + str(pts_eq2[3])
    else:
        score_q1 = None
        score_q2 = None
        score_q3 = None
        score_q4 = None

    result = getScores(soup)

    home_team, away_team = getTeams(soup)

    court, city, region = getLocation(soup)
    place = city + ', ' + region

    game = Game(home_team, away_team, result, date_played, referee_1, referee_2, referee_3, place, court, score_q1, score_q2, score_q3, score_q4, None, True, 'processing')
    return game


