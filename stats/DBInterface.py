import mysql.connector
from mysql.connector import Error


def checkLeagueStateInDB(leagueName):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "select id, state_statistics from leagues where name='{}'"\
            .format(leagueName)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                if not(len(records)):
                    return [None, 'not_inserted']
                elif len(records)==1:
                    return records[0]
                else:
                    print('Error in game, more than two options' + leagueName)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertLeagueInDB(leagueName, type, gender):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "INSERT INTO leagues (name, type, gender, state_statistics) VALUES ('{}', '{}', '{}', 'processing')"\
            .format(leagueName, type, gender)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute('select LAST_INSERT_ID()')
            records = cursor.fetchall()
            return int(records[0][0]) #league_id




    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def updateLeagueInDB(leagueid):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "UPDATE leagues SET state_statistics='finished' WHERE id={}"\
            .format(leagueid)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def checkSeasonStateInDB(leagueid, years):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "select id, state_statistics from seasons where league_id = {} and years = '{}'"\
            .format(leagueid, years)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                if not(len(records)):
                    return [None, 'not_inserted']
                elif len(records)==1:
                    return records[0]
                else:
                    print('Error in season, more than two options' + years)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertSeasonInDB(leagueid, years):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "INSERT INTO seasons (years, league_id, state_statistics) VALUES ('{}', {}, 'processing')"\
            .format(years, leagueid)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute('select LAST_INSERT_ID()')
            records = cursor.fetchall()
            return int(records[0][0]) #league_id



    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def updateSeasonInDB(seasonid):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "UPDATE seasons SET state_statistics='finished' WHERE id={}"\
            .format(seasonid)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def checkGroupStateInDB(seasonid, name):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "select id, state_statistics from `groups` where season_id = {} and group_name = '{}'"\
            .format(seasonid, name)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                if not(len(records)):
                    return [None, 'not_inserted']
                elif len(records)==1:
                    return records[0]
                else:
                    print('Error in season, more than two options' + name, ' season id ' + seasonid)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertGroupInDB(seasonid, name):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "INSERT INTO `groups` (group_name, season_id, state_statistics) VALUES ('{}', {}, 'processing')"\
            .format(name, seasonid)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute('select LAST_INSERT_ID()')
            records = cursor.fetchall()
            return int(records[0][0]) #league_id



    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def updateGroupInDB(groupid):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "UPDATE `groups` SET state_statistics='finished' WHERE id={} "\
            .format(groupid)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def checkJornadaStateInDB(groupid, jornada):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "select id, state_statistics from jornadas where group_id = {} and jornada = '{}'"\
            .format(groupid, jornada)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                if not(len(records)):
                    return [None, 'not_inserted']
                elif len(records)==1:
                    return records[0]
                else:
                    print('Error in season, more than two options' + jornada)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertJornadaInDB(groupid, jornada):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "INSERT INTO jornadas (jornada, group_id, state_statistics) VALUES ({}, {}, 'processing')"\
            .format(jornada, groupid)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute('select LAST_INSERT_ID()')
            records = cursor.fetchall()
            return int(records[0][0]) #league_id



    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def updateJornadaInDB(jornadaid):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "UPDATE jornadas SET state_statistics='finished' WHERE id = {} "\
            .format(jornadaid)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e, " Updating jornada with jornada_id" + jornadaid)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()



def checkGameStateInDB(jornadaid, game): #To be checked with home_team and away_team
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "select id, state_statistics from games where jornada_id = {} and home_team = '{}' and away_team = '{}'"\
            .format(jornadaid, game['home_team'], game['away_team'])

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                records = cursor.fetchall()
                if not(len(records)):
                    return [None, 'not_inserted']
                elif len(records)==1:
                    return records[0]
                else:
                    print('Error in game, more than two options: jornada_id: ' + jornadaid + ', game: ' + game)

    except Error as e:
        print("Error while connecting to MySQL", e, " checking game with jornada_id " + jornadaid + " game" + game)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertGameInDB(jornadaid, game):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "INSERT INTO games (jornada_id, home_team, away_team, result, date_played, referee_1, referee_2, referee_3, place, court, score_q1, score_q2, score_q3, score_q4, state_statistics) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 'processing')"\
            .format(jornadaid, game['home_team'], game['away_team'], game['result'], game['date_played'].strftime('%Y-%m-%d %H:%M:%S'), game['referee_1'], game['referee_2'], game['referee_3'], game['place'], game['court'], game['score_q1'], game['score_q2'], game['score_q3'], game['score_q4'])

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute('select LAST_INSERT_ID()')
            records = cursor.fetchall()
            return int(records[0][0]) #league_id



    except Error as e:
        print("Error while connecting to MySQL", e, ": Insert game with jornada_id: " + jornadaid + " game: " + game)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def updateGameInDB(gameid):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "UPDATE games SET state_statistics='finished' WHERE id={} "\
            .format(gameid)

        if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

    except Error as e:
        print("Error while connecting to MySQL: ", e, " UPDATE GAME WITH GAMEID: ", gameid)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


def removeAllStatsInDB(gameid):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )
        cursor = connection.cursor()
        sql_Delete_query = """Delete from stats where game_id = {}""".format(gameid)
        cursor.execute(sql_Delete_query)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to Delete record from table: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertStatsInDB(gameid, stats):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        if "'" in stats['PLAYER']:
            stats['PLAYER'] = stats['PLAYER'].replace("'","")

        query = "INSERT INTO stats (game_id, team, PLAYER, NUMBER, starter, MIN, PTS, 2PA, 2PM, 3PA, 3PM, FTA, FTM, DREB, OREB, AST, STL, TOV, BLKM, BLKR, DNK, PFR, PFM, VAL, PM) VALUES ({}, '{}', '{}', {}, {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"\
            .format(gameid, str(stats['team']), str(stats['PLAYER']), int(stats['NUMBER']), int(stats['starter']), str(stats['MIN']) , int(stats['PTS']), int(stats['2PA']), int(stats['2PM']), int(stats['3PA']), int(stats['3PM']), int(stats['FTA']) , int(stats['FTM']), int(stats['DREB']), int(stats['OREB']), int(stats['AST']), int(stats['STL']), int(stats['TOV']), int(stats['BLKM']), int(stats['BLKR']), int(stats['DNK']), int(stats['PFR']), int(stats['PFM']), int(stats['VAL']), int(stats['PM']))

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

    except Error as e:
        print("Error while connecting to MySQL ", e, " to put stats in with game_id " + gameid + " and player " + stats)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


