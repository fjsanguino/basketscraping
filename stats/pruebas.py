import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from utils import file_name

#TODO: iterate for all years/competitions

#TODO: iterate for all the jornadas
#TODO: check if the jornada is already done

'''Sends a GET HTTP request to the given URL'''
URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=5&t=2019'
page = requests.get(URL)

'''Parses the recieved information (HTML in this case) to BeautifulSoup'''
soup = BeautifulSoup(page.content, 'html.parser')

'''Gets the results table (RESULTADOS in example image)'''
results = soup.find("div", {"class": "contentTablaDataGrid"})
print(results.prettify())

'''Too much code, only to get which jornada we are getting the data'''
jornada = results.div.string[results.div.string.find('Jornada')+8: results.div.string.find('Jornada')+10]
print('Jornada', jornada)

'''Finds all the URL to the statistics of each game of the jornada'''
links = results.table.find_all('a')
#print(links)

'''Gets all the links to the statistics of each game'''
l = []
for link in links:
    if not(link['href'].find('Partido')):
        l.append('http://competiciones.feb.es/estadisticas/' + link['href'])

'''Goes over every game found'''
for li in l:
    #print(li)
    page = requests.get(li) #Sends a GET HTTP request

    soup = BeautifulSoup(page.content, 'html.parser') #Parses the content using a HTML canvas

    #TODO: get all the information from the game: place (pista y localidad), marcadores parciales, marcador total, fecha y hora,
    #TODO: check if the game is already in the file

    '''Iterates over the tables found that have stats'''
    table = soup.find("table", {"class": "tablaDataGrid"})
    #print(table.prettify())
    counttables = 0
    while table != None:
        counttables = counttables + 1
        '''Variable defition'''
        titular = []
        num_jug = []
        nombre = []
        min = []
        pts = []
        zone_made= []
        zone_throw = []
        trip_made = []
        trip_throw = []
        free_made = []
        free_throw = []
        reb_def = []
        reb_of = []
        assist = []
        recu = []
        perd = []
        tap_made = []
        tap_rec = []
        dunk = []
        foul_made = []
        foul_rec = []
        val = []
        masmenos = []

        '''Gets all the data'''
        a = table.tr
        a = a.next_sibling #Needed beacuse the first <tr> is an empty string
        while a.next_sibling.next_sibling != None:
                b = a.td

                c = 0
                for i in range(18):
                    if i == 0: #Titular o no
                        tit = False
                        if b.string == None:
                            tit = True
                        #print('Titular:', tit)
                        titular.append(tit)
                    if i == 1: #Numero de jugador
                        #print('Num jug:', b.span.string)
                        num_jug.append(b.span.string)
                    if i == 2: #Nombre jugador
                        #print('nombre:', b.a.string)
                        nombre.append(b.a.string)
                    if i == 3: #Minutos jugados
                        #print('Min:', b.span.string)
                        min.append(b.span.string)
                    if i == 4: #Puntos anotados
                        #print('Puntos:', b.span.string)
                        pts.append(b.span.string)
                    if i == 5: #2pts(anotados/intentados) porcentaje%
                        #print('2pts:', b.span.string)
                        zone = b.span.string
                        zone_made.append(zone[zone.find('/')-1])
                        zone_throw.append(zone[zone.find('/')+1])
                    if i == 6: #3pts(anotados/intentados) porcentaje%
                        #print('3pts:', b.span.string)
                        trip = b.span.string
                        trip_made.append(trip[trip.find('/')-1])
                        trip_throw.append(trip[trip.find('/')+1])
                    if i == 7: #Tiros campo(anotados/intentados) porcentaje%
                        hola = 1
                        #print('Campo:', b.span.string)
                    if i == 8: #T.L.(anotados/intentados) porcentaje%
                        #print('T.L:', b.span.string)
                        free = b.span.string
                        free_made.append(free[free.find('/')-1])
                        free_throw.append(free[free.find('/')+1])
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
                        reb_def.append(reb[0])
                        reb_of.append(reb[1])
                    if i == 10: #Asistencias
                        #print('As:', b.span.string)
                        assist.append(b.span.string)
                    if i == 11: #Balones recuperados
                        #print('Recuperados:', b.span.string)
                        recu.append(b.span.string)
                    if i == 12: #Balones perdidos
                        #print('perdidos:', b.span.string)
                        perd.append(b.span.string)
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
                        tap_made.append(tap[0])
                        tap_rec.append(tap[1])
                    if i == 14: #Mates
                        #print('Mates:', b.span.string)
                        dunk.append(b.span.string)
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
                        foul_made.append(fal[0])
                        foul_rec.append(fal[1])
                    if i == 16: #Valoracion
                        #print('Valoracion:', b.span.string)
                        val.append(b.span.string)
                    if i == 17: #+/-
                        #print('+/-:', b.span.string)
                        masmenos.append(b.span.string)
                    b = b.next_sibling

                a = a.next_sibling

        '''Crea diccionario con todos los nombres'''
        d = {'Nombre': nombre, 'Numero': num_jug, 'Titular': titular, 'Minutos': min, 'Puntos': pts,
             '2ptsmade': zone_made, '2ptstried': zone_throw, '3ptsmade': trip_made, '3ptstried': trip_throw,
             'TLmade': free_made, 'TLtried': free_throw, 'RebDef': reb_def, 'RebOf': reb_of, 'Asistencias': assist,
             'Recuperados': recu, 'Perdidos': perd, 'TapMade': tap_made, 'TapRecieved': tap_rec, 'Mates': dunk,
             'FaltasCometidas': foul_made, 'FaltasRecibidas': foul_rec, 'Valoracion': val, '+/-': masmenos}

        '''Transforma diccionario en DataFrame de Pandas, cada fila son los datos un jugador determinado 
        y cada columna nombres, numeros, si es titular...'''
        df = pd.DataFrame(data=d)

        '''Crea un csv con los resultados de la jornada '''
        filename = file_name('jornada' + jornada, table.previous_sibling.previous_sibling.string) #with the utils archive calculates the name of the csv file
        print(filename)
        if (not os.path.exists(filename[:filename.find('/')])):
            os.mkdir(filename[:filename.find('/')])
        df.to_csv(filename, index=False)

        '''Find the next table to get the stats'''
        table = table.findNext("table", {"class": "tablaDataGrid"})
