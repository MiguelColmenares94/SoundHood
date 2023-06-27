import mysql.connector


class MySQLConnection:
    __config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'soundhood',
        'pool_name': 'soundhood_pool',
        'pool_size': 5
    }

    def __init__(self):
        try:
            pool = mysql.connector.pooling.MySQLConnectionPool(**self.__config)
            self.connection = pool.get_connection()
            print('Successfully connected to MySQL database')
        except mysql.connector.Error as e:
            print('Error while connecting to the database: ', str(e))
            raise e

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
