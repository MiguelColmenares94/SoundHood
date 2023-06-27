from models.user import User
from models.engine.mysql_connection import MySQLConnection
from flask import session
from mysql.connector.errors import Error


class UserDAO:
    __db_storage = None

    def __init__(self):
        try:
            self.__db_storage = MySQLConnection()
        except Error as e:
            raise e


    def get_user_by_spotify_id(self):
        conn = None
        user = None
        try:
            conn = self.__db_storage.get_connection()
            query = """
                SELECT
                    user_name,
                    profile_photo,
                    country
                FROM User
                WHERE spotify_user_id = %s"
            """
            cursor = conn.cursor()
            cursor.execute(query, (session['user_id'],))
            result = cursor.fetchone()

            if result:
                user = User(
                    user_name=result[0],
                    profile_photo=result[1],
                    country=result[2]
                )

        except Error as e:
            print('Error: ' + str(e))
            if self.__conn:
                self.__conn.close_connection()

        return user
