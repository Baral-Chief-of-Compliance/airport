from django.conf import settings
import pymysql
import logging

# класс соединения с бд
class DB_connection(object):

    #соединение
    connection : pymysql.connect

    #логгер
    logger : logging.Logger

    # конструктор, который при создании создает подключение к бд и логер
    def __init__(self) -> None:
        self.logger = logging.getLogger('main')

        try:
            host = settings.AIROPORT_MYSQL_HOST
            user = settings.AIROPORT_MYSQL_USER
            password = settings.AIROPORT_MYSQL_PASSWORD
            database = settings.AIROPORT_MYSQL_DB
            port = int(settings.AIROPORT_MYSQL_PORT)

            self.connection = pymysql.connect(
                                    host=host,
                                    user=user,
                                    password=password,
                                    database=database,
                                    cursorclass=pymysql.cursors.DictCursor,
                                    port=port
                                )
        except Exception as e:
            self.logger.error(f'Error in connection to db(host: {host}, user: {user}, pass: {password}, db: {database}, port: {port}): {e}')


        

    #реализация select c fetchall
    def select_fetchall(self, sql_query: str, sql_params: tuple = ()) -> tuple:
        result: tuple = ()

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql_query, sql_params)
            result = cursor.fetchall()
        except Exception as e:
            self.logger.error(f'Error in select_fetchall in: {sql_query} with parameters: {sql_params} error: {e}')

        return result
    

    #реализация select с fetchone
    def select_fetchone(self, sql_query: str, sql_params: tuple = ()) -> tuple:
        result_one : tuple = ()

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql_query, sql_params)
            result_one = cursor.fetchone()
        except Exception as e:
            self.logger.error(f'Error in select_fetchone in: {sql_query} with parameters: {sql_params} error: {e}')

        return result_one
    
    #реализация sql запроса с commit
    def sql_query_with_commit(self, sql_query: str, sql_params: tuple = ()) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql_query, sql_params)
            self.connection.commit()
        except Exception as e:
            self.logger.error(f'Error in select_fetchone in: {sql_query} with parameters: {sql_params} error: {e}')


    #деструктор, закрывает соединение при удаление объекта 
    def __del__(self) -> None:
        self.connection.close()