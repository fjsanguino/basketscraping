import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

'''Sends a GET HTTP request to the given URL'''
# PARTIDO DE EJEMPLO
URL = 'http://competiciones.feb.es/estadisticas/Partido.aspx?p=2097555&med=0'
page = requests.get(URL)

'''Parses the recieved information (HTML in this case) to BeautifulSoup'''
soup = BeautifulSoup(page.content, 'html.parser')


def getDate():
    # dia, mes, año
    dia = [int(e) for e in soup.find("span", {"id": "fechaLabel"}).text.split('/')]
    # hora, min
    hora = [int(e) for e in soup.find("span", {"id": "horaLabel"}).text.split(':')]
    # datetime(year, month, day, hour, minute, second, microsecond)
    fecha = datetime(dia[2], dia[1], dia[0], hora[0], hora[1])
    return fecha

def getReferees():
    arbitroP = str(soup.find("span", {"id": "arbitroPrincipalLabel"}).text)
    arbitroA1 = str(soup.find("span", {"id": "arbitroAuxiliarLabel"}).text)
    arbitroA2 = str(soup.find("span", {"id": "arbitroAuxiliar2Label"}).text)
    arbitros = [arbitroP[0:arbitroP.index(',')], arbitroA1[0:arbitroA1.index(',')], arbitroA2[0:arbitroA2.index(',')]]

    return arbitros

def getTeams():
    table_cuartos = soup.find("table", {"class": "tablaResultadosCuartos"})
    home_team = str(table_cuartos.find_all('span')[0].text)
    away_team = str(table_cuartos.find_all('span')[5].text)
    return home_team, away_team

def getResult():
    table_cuartos = soup.find("table", {"class": "tablaResultadosCuartos"})
    pts_eq1 = [int(e.text) for e in table_cuartos.find_all('span')[1:5]]
    pts_eq2 = [int(e.text) for e in table_cuartos.find_all('span')[6:10]]
    return pts_eq1, pts_eq2

def getScores():
    
    resultLocal = int(soup.find("span", {"id": "resultadoLocalLabel"}).text)
    resultVisitante = int(soup.find("span", {"id": "resultadoVisitanteLabel"}).text)
    # resultado como lista de enteros
    result2 = [int(soup.find("span", {"id": "resultadoLocalLabel"}).text), int(soup.find("span", {"id": "resultadoVisitanteLabel"}).text)]
    # resultado como concatenacion de strings
    result = str(resultLocal) + ' - ' + str(resultVisitante)
    return result

def getLocation():
    court = str(soup.find("span", {"id": "pistaJuegoLabel"}).text)
    city = str(soup.find("span", {"id": "localidadLabel"}).text)
    region = str(soup.find("span", {"id": "provinciaLabel"}).text)
    return court, city, region



def getMatchData(league_id, jornada):
    #table_match = soup.find("div", {"class": "fichaPartido"})
    fecha = getDate()

    arbitroP, arbitroA1, arbitroA2 = getReferees()

    home_team, away_team = getTeams()
    pts_eq1, pts_eq2 = getResult()
    score_q1 = str(pts_eq1[0]) + ' - ' + str(pts_eq2[0]) 
    score_q2 = str(pts_eq1[1]) + ' - ' + str(pts_eq2[1]) 
    score_q3 = str(pts_eq1[2]) + ' - ' + str(pts_eq2[2]) 
    score_q4 = str(pts_eq1[3]) + ' - ' + str(pts_eq2[3]) 
    result = getScores()
    
    court, city, region = getLocation()
    place = city + ', ' + region
    state = 'Spain'

    d = {"home_team": home_team, "away_team": away_team, "result": result, "date": fecha, "league_id": league_id, "jornada": jornada, "referee_1": arbitroP, "referee_2": arbitroA1, "referee_3": arbitroA2, "place": place, "court": court, "score_q1": score_q1, "score_q2": score_q2, "score_q3": score_q3, "score_q4": score_q4, "state": state}

    df = pd.DataFrame(data=d, index=[0])

    print(df)


# SE NECESITA PASAR "league_id" y "jornada"
# 3 y 12 inventadas de ejemplo
getMatchData(3,12)