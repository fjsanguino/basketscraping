import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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
    table_cuartos = soup.find("table", {"class": "tablaResultadosCuartos"})
    if table_cuartos == None:
        return None, None
    home_team = str(table_cuartos.find_all('span')[0].text)
    away_team = str(table_cuartos.find_all('span')[5].text)
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

def getGameDataFromGameURL(URL, jornada_id):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    fecha = getDate(soup)

    arbitroP, arbitroA1, arbitroA2 = getReferees(soup)

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

    d = {"home_team": home_team, "away_team": away_team, "result": result, "date_played": fecha, "jornada_id": jornada_id, "referee_1": arbitroP, "referee_2": arbitroA1, "referee_3": arbitroA2, "place": place, "court": court, "score_q1": score_q1, "score_q2": score_q2, "score_q3": score_q3, "score_q4": score_q4}

    return d

# SE NECESITA PASAR "league_id" y "jornada"
# 3 y 12 inventadas de ejemplo
#URL = 'http://competiciones.feb.es/estadisticas/Partido.aspx?p=2097555&med=0'

#getGameDataFromGameURL(URL, 78)

