import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = 'http://competiciones.feb.es/estadisticas/default.aspx'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

def getLinks():
    table_comp = soup.find("div", {"class": "navegarCompeticiones"})
    l = []
    for e in table_comp.find_all("a"):
        if 'resultados' in e['href'].lower():
            l.append('http://competiciones.feb.es/estadisticas/' + e['href'])
    return l

def getSeason(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    temporadas = soup.find("select", {"id": "temporadasDropDownList"})
    t = []
    for e in temporadas.find_all('option'):
        t.append((e.text).replace('/','-'))
    return t

def getGender(name):
    name = name.lower()
    if 'femenino' in name or 'femenina' in name:
        return 'female'
    elif 'masculino' in name or 'masculina' in name:
        return 'male'
    else:
        return 'male'
    
def getType(name):
    posible_types = ['Mini','Amateur', 'Semiprofesional', 'Profesional']
    leagues = ['mini','infantil','cadete', 'sub', 'eba', 'liga femenina', 'leb']
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
    

def getLeagueNames():

    table_comp = soup.find("div", {"class": "navegarCompeticiones"})
    leagues = []
    for e in table_comp.find_all("li", {"class": "competicion"}):
        if(int(e.text.find('['))!=-1):
            leagues.append(str(e.text[0:e.text.index('[')]))
        else:
            leagues.append(str(e.text))
    return leagues


def main():
    start = datetime.now()

    df = pd.DataFrame(columns=['name','season','type','gender','state'])
    leagues = []
    links = getLinks()
    reps = []
    for e in links:
        reps.append(len(getSeason(e)))
    #print(getLeagueNames()[0])
    i = 0
    for league in reps:
        #print(league)
        for n_season in range(league):
            
            l = getLeagueNames()[i]
            s = getSeason(links[i])[n_season]
            t = getType(l)
            g = getGender(l)
            state = 'Spain'
            #print(getSeason(links[i]))
            leagues.append((l,s,t,g,state))
            #print((l,s,t,g,state))
            df.loc[len(df)] = [l, s, t, g, state]
            #print(df)
        i += 1
    
    print(df)
    end = datetime.now()
    time = end - start
    print(time)
    # 


    

# getSeason('http://competiciones.feb.es/estadisticas/Resultados.aspx?g=1&t=2019')
# getLinks()
# getLeagueNames()
main()
