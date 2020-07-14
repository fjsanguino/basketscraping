import mysql.connector
from mysql.connector import Error

def getSeasonID(liga_name, season):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "select seasons.id from leagues, seasons where leagues.id = league_id and name = '{}' and years = '{}'"\
            .format(liga_name, season)

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


def updateGame(downloadurl, gameid):
    try:
        connection = mysql.connector.connect(
            host="remotemysql.com",
            user="g3GJdRGWE4",
            passwd="4I1ZMfcMXg",
            database="g3GJdRGWE4"
        )

        query = "UPDATE games SET is_video=1, state_video='processing', download_url='{}'  WHERE id={} "\
            .format(downloadurl, gameid)

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
