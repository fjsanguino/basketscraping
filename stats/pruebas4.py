import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import re

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from utils import file_name2, getJornadaFromJornadaURL
from game import getGameDataFromGameURL
from league import getLeaguesURLFromMainURL
import DBInterface



def getJornadaURLFromJornadaNameStr(busq, j, driver):
    j_el = driver.find_element_by_id("jornadasDropDownList")
    for option in j_el.find_elements_by_tag_name('option'):
        if str(busq) in option.text:
            if(j>1):
                option.click()

            break
    
def getGroupURLFromGroupNameStr(busq, driver):
    g_el = driver.find_element_by_id("gruposDropDownList")
    for option in g_el.find_elements_by_tag_name('option'):
        if str(busq)in option.text:
            option.click()
            break
    
def getSeasonURLFromYearStr(busq, driver):
    t_el = driver.find_element_by_id("temporadasDropDownList")
    for option in t_el.find_elements_by_tag_name('option'):
        if str(busq)in option.text:
            option.click()
            break

#returns jornada (str with the jornada) and list with the links to the games
def getGamesURLFromJornadaURL(soup):
    results = soup.find("div", {"class": "contentTablaDataGrid"})
    jornada = getJornadaFromJornadaURL(results)
    links = results.table.find_all('a')
    l = []
    for link in links:
        if not(link['href'].find('Partido')):
            l.append('http://competiciones.feb.es/estadisticas/' + link['href'])
    #print(l)
    return jornada, l

def exportData(temporada, grupo, jornada, table, df):
    '''Crea un csv con los resultados de la jornada '''
    filename = file_name2(table.previous_sibling.previous_sibling.string) #with the tils archive calculates the name of the csv file
    print(temporada)
    print(grupo)
    print(jornada)
    print(filename)
    
    if (not os.path.exists(os.path.join(str(temporada), str(grupo), str(jornada)))):
        os.makedirs(os.path.join(str(temporada), str(grupo), str(jornada)))
    print(os.getcwd())
    df.to_csv(os.path.join(str(temporada), str(grupo), str(jornada))+'/'+filename, index=False)
    #if(not os.path.exists(temporada)):
    #os.makedirs(os.path.join(temporada,grupo,jornada,filename)
    #df.to_csv(filename, index=False)
    #if (not os.path.exists(filename[:filename.find('/')])):
        #os.mkdir(str(temporada)+'/'+str(grupo)+filename[:filename.find('/')])
    #df.to_csv(filename, index=False)

def getStatsFromGameURL(gameURL, jornada_id):

        page = requests.get(gameURL) #Sends a GET HTTP request

        soup = BeautifulSoup(page.content, 'html.parser') #Parses the content using a HTML canvas

        game_data = getGameDataFromGameURL(URL, jornada_id)

        '''check if season in database'''
        game_state = DBInterface.checkGameStateInDB(jornada_id, game_data)
        if game_state[1] == 'finished':
            return
        elif game_state[1] == 'processing':
            game_id = game_state[0]
            DBInterface.removeAllStatsInDB(game_id)
        elif game_state[1] == 'not_inserted':
            game_id = DBInterface.insertGameInDB(jornada_id, game_data)
        else:  # error
            return

        '''Iterates over the tables found that have stats'''
        table = soup.find("table", {"class": "tablaDataGrid"})
        #print(table.prettify())
        counttables = 0
        while table != None:
            counttables = counttables + 1

            '''Gets all the data'''
            a = table.tr
            a = a.next_sibling #Needed beacuse the first <tr> is an empty string
            while a.next_sibling.next_sibling != None:
                    b = a.td

                    c = 0
                    '''Variable defition'''
                    stat = {}
                    for i in range(18):
                        if i == 0: #Titular o no
                            tit = False
                            if b.string == None:
                                tit = True
                            #print('Titular:', tit)
                            stat['starter'] = (tit)
                        if i == 1: #Numero de jugador
                            #print('Num jug:', b.span.string)
                            stat['NUMBER'] = (b.span.string)
                        if i == 2: #Nombre jugador
                            #print('nombre:', b.a.string)
                            stat['PLAYER'] = (b.a.string)
                        if i == 3: #Minutos jugados
                            #print('Min:', b.span.string)
                            stat['MIN'] = (b.span.string)
                        if i == 4: #Puntos anotados
                            #print('Puntos:', b.span.string)
                            stat['PTS'] = (b.span.string)
                        if i == 5: #2pts(anotados/intentados) porcentaje%
                            #print('2pts:', b.span.string)
                            zone = b.span.string
                            stat['2PM'] = (zone[zone.find('/')-1])
                            stat['2PA'] = (zone[zone.find('/')+1])
                        if i == 6: #3pts(anotados/intentados) porcentaje%
                            #print('3pts:', b.span.string)
                            trip = b.span.string
                            stat['3PM'] = (trip[trip.find('/')-1])
                            stat['3PA'] = (trip[trip.find('/')+1])
                        if i == 7: #Tiros campo(anotados/intentados) porcentaje%
                            hola = 1
                            #print('Campo:', b.span.string)
                        if i == 8: #T.L.(anotados/intentados) porcentaje%
                            #print('T.L:', b.span.string)
                            free = b.span.string
                            stat['FTM'] = (free[free.find('/')-1])
                            stat['FTA'] = (free[free.find('/')+1])
                        if i == 9: #Rebotes, def of to
                            c = b.td
                            #print(b)
                            reb = []
                            count = 0
                            while c.next_sibling != None:
                                count = count + 1
                                if count % 2 == 1: #I dont know why but the odd children are empty strings
                                    reb.append(c.span.string)
                                c = c.next_sibling
                            #print('Reb: ', reb)
                            stat['DREB'] = (reb[0])
                            stat['OREB'] = (reb[1])
                        if i == 10: #Asistencias
                            #print('As:', b.span.string)
                            stat['AST'] = (b.span.string)
                        if i == 11: #Balones recuperados
                            #print('Recuperados:', b.span.string)
                            stat['STL'] = (b.span.string)
                        if i == 12: #Balones perdidos
                            #print('perdidos:', b.span.string)
                            stat['TOV'] = (b.span.string)
                        if i == 13: #Tapones, favor contra
                            c = b.td
                            tap = []
                            count= 0
                            while c.next_sibling != None:
                                count = count + 1
                                if count % 2 == 1:
                                    tap.append(c.span.string)
                                c = c.next_sibling
                            #print('Tap:', tap)
                            stat['BLKM'] = (tap[0])
                            stat['BLKR'] = (tap[1])
                        if i == 14: #Mates
                            #print('Mates:', b.span.string)
                            stat['DNK'] = (b.span.string)
                        if i == 15: #Faltas, cometidas recibidas
                            c = b.td
                            fal = []
                            count = 0
                            while c.next_sibling != None:
                                count = count + 1
                                if count % 2 == 1:  # I dont know why but the odd children are empty strings
                                    fal.append(c.span.string)
                                #print(c)
                                c = c.next_sibling
                            #print('fouls', fal)
                            stat['PFM'] = (fal[0])
                            stat['PFR'] = (fal[1])
                        if i == 16: #Valoracion
                            #print('Valoracion:', b.span.string)
                            stat['VAL'] = (b.span.string)
                        if i == 17: #+/-
                            #print('+/-:', b.span.string)
                            stat['+/-'] = (b.span.string)
                        b = b.next_sibling

                        '''Inserts Data in Database'''
                        DBInterface.insertStatsInDB(game_id, stat)

                    a = a.next_sibling


            '''Find the next table to get the stats'''
            table = table.findNext("table", {"class": "tablaDataGrid"})

        DBInterface.updateGameInDB(game_id)

def getStatsFromLeagueURL(mainURL,leagueURL, league_id):
    driver = webdriver.Firefox()
    driver.get(mainURL)
    path = leagueURL[leagueURL.rfind('/')+1:]
    print(path)
    driver.find_element_by_xpath("//a[@href='{}']".format(path)).click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    seasons_html = soup.find("select", {"id": "temporadasDropDownList"})

    for s in seasons_html.find_all('option'):
        s_e = (s.string).replace('/', '-')

        getSeasonURLFromYearStr(s_e, driver)

        '''check if season in database'''
        season_state = DBInterface.checkSeasonStateInDB(league_id, s_e)
        if season_state[1] == 'finished':
            break
        elif season_state[1] == 'processing':
            season_id = season_state[0]
        elif season_state[1] == 'not_inserted':
            season_id = DBInterface.insertSeasonInDB(league_id, s_e)
        else:  # error
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')  # html from the main page of the league (season)
        groups_html = soup.find("select", {"id": "gruposDropDownList"})
        for g in groups_html.find_all('option'):
            g_e = g.string

            getGroupURLFromGroupNameStr(g_e, driver)

            '''check if group in database'''
            group_state = DBInterface.checkGroupStateInDB(season_id, g_e)
            if group_state[1] == 'finished':
                break
            elif group_state[1] == 'processing':
                group_id = group_state[0]
            elif group_state[1] == 'not_inserted':
                group_id = DBInterface.insertGroupInDB(season_id, g_e)
            else:  # error
                break

            soup = BeautifulSoup(driver.page_source, 'html.parser')  # html from the main page of the group
            jornadas_html = soup.find("select", {"id": "jornadasDropDownList"})
            j = len(jornadas_html.find_all('option'))
            for e in jornadas_html.find_all('option'):
                j_e = e.string

                getJornadaURLFromJornadaNameStr(j_e, j, driver)

                #TODO: check if jornada in dataBase
                '''check if jornada in database'''
                jornada_state = DBInterface.checkJornadaStateInDB(group_id, j_e)
                if jornada_state[1] == 'finished':
                    break
                elif jornada_state[1] == 'processing':
                    jornada_id = jornada_state[0]
                elif jornada_state[1] == 'not_inserted':
                    jornada_id = DBInterface.insertJornadaInDB(group_id, j_e)
                else:  # error
                    break

                soup = BeautifulSoup(driver.page_source, 'html.parser')  # html from the main page of the jornada
                jornada, gamesURL = getGamesURLFromJornadaURL(soup)
                print(gamesURL)
                print(s_e)
                print(g_e)
                print(j_e)
                for g_url in gamesURL:
                    getStatsFromGameURL(g_url, jornada_id)
                    exit(0)

                '''update jornada state to finish in database'''
                DBInterface.updateJornadaInDB(jornada_id)

            '''update group state to finish in database'''
            DBInterface.updateGroupInDB(group_id)

        '''update season state to finish in database'''
        DBInterface.updateGroupInDB(season_id)

    '''update league state to finish'''
    DBInterface.updateLeagueInDB(league_id)

    driver.close()
    driver.quit()


if __name__=='__main__':
    URL = 'http://competiciones.feb.es/estadisticas/default.aspx'

    leagueids, leagueURLs = getLeaguesURLFromMainURL(URL)
    for i in range(len(leagueids)):
        print(leagueids[i], leagueURLs[i])
        getStatsFromLeagueURL(URL, leagueURLs[i], leagueids[i])


