import os
import re

def file_name(jornada, string):
    if string == 'NÁUTICO TENERIFE':
        file = 'tenerife'
    elif string == 'MOVISTAR ESTUDIANTES':
        file = 'estudiantes'
    elif string == 'ESTUDIO':
        file = 'estudio'
    elif string == 'NCS ALCOBENDAS':
        file = 'alcobendas'
    elif string == 'ISOVER BASKET AZUQUECA':
        file = 'azuqueca'
    elif string == 'UROS DE RIVAS':
        file = 'rivas'
    elif string == 'ZENTRO BASKET MADRID':
        file = 'zentrobasket'
    elif string == 'REAL MADRID':
        file = 'realmadrid'
    elif string == 'GLOBALCAJA QUINTANAR':
        file = 'quintanar'
    elif string == 'TOBARRA CLUB DE BALONCESTO':
        file = 'tobarra'
    elif string == 'LUJISA GUADALAJARA BASKET':
        file = 'guadalajara'
    elif string == 'BALONCESTO ALCALA':
        file = 'alcala'
    elif string == 'ALOE PLUS LANZAROTE CONEJEROS':
        file = 'lanzarote'
    elif string == 'DISTRITO OLIMPICO':
        file = 'distritoolimpico'
    elif string == 'C.B. POZUELO ARRABE ASESORES':
        file = 'pozuelo'
    elif string == 'CB AGÜIMES':
        file = 'aguimes'
    else:
        print('error with ' + string)
        exit(1)

    return os.path.join(jornada, file) + '.csv'

def file_name2(string):
    if string == 'NÁUTICO TENERIFE':
        file = 'tenerife'
    elif string == 'MOVISTAR ESTUDIANTES':
        file = 'estudiantes'
    elif string == 'ESTUDIO':
        file = 'estudio'
    elif string == 'NCS ALCOBENDAS':
        file = 'alcobendas'
    elif string == 'ISOVER BASKET AZUQUECA':
        file = 'azuqueca'
    elif string == 'UROS DE RIVAS':
        file = 'rivas'
    elif string == 'ZENTRO BASKET MADRID':
        file = 'zentrobasket'
    elif string == 'REAL MADRID':
        file = 'realmadrid'
    elif string == 'GLOBALCAJA QUINTANAR':
        file = 'quintanar'
    elif string == 'TOBARRA CLUB DE BALONCESTO':
        file = 'tobarra'
    elif string == 'LUJISA GUADALAJARA BASKET':
        file = 'guadalajara'
    elif string == 'BALONCESTO ALCALA':
        file = 'alcala'
    elif string == 'ALOE PLUS LANZAROTE CONEJEROS':
        file = 'lanzarote'
    elif string == 'DISTRITO OLIMPICO':
        file = 'distritoolimpico'
    elif string == 'C.B. POZUELO ARRABE ASESORES':
        file = 'pozuelo'
    elif string == 'CB AGÜIMES':
        file = 'aguimes'
    else:
        print('error with ' + string)
        exit(1)

    return os.path.join(file) + '.csv'


def getJornadaFromJornadaURL(results):
    #jornada = results.div.string[results.div.string.find('Jornada')+8: results.div.string.find('Jornada')+10]
    # mejor asi para eliminar parentesis y texto
    jornada = re.sub("[\(\[].*?[\)\]]", "", results.div.string).replace('Resultados ','')
    print(jornada)
    return jornada
