from .main import DB_connection


# получить все авикомпании
def get_all_airlines() -> list :
    airlines: list = []

    db_con = DB_connection()

    sql_airlines: tuple = db_con.select_fetchall(
        sql_query='SELECT * FROM `Авиакомпания` ORDER BY `Название авиакомпании`'
    )

    del db_con

    for sa in sql_airlines:
        airlines.append(
            {
                'airline_name': sa['Название авиакомпании'],
                'airline_tarif': sa['Тариф'] 
            }
        )

    return airlines


# получить все аивиавкомпании для select flight form
def get_all_airlines_for_flight_form() -> list:
    airlines: list = []
    db_con = DB_connection()

    sql_airlines: tuple = db_con.select_fetchall(
        sql_query='SELECT `Название авиакомпании` FROM `Авиакомпания` ORDER BY `Название авиакомпании`'
    )

    del db_con

    for sa in sql_airlines:
        airlines.append(
            (
                sa['Название авиакомпании'],
                sa['Название авиакомпании'],
            )
        )   
    return airlines


#получитть конкретную авикомпанию по её названию
def get_one_airline(airline_name: str) -> dict:
    airline: dict = {}

    db_con = DB_connection()

    sql_airline: tuple = db_con.select_fetchone(
        sql_query='SELECT * FROM `Авиакомпания` WHERE `Название авиакомпании`=%s',
        sql_params=(airline_name,)
    )

    del db_con

    airline = {
        'airline_name': sql_airline['Название авиакомпании'],
        'airline_tarif': sql_airline['Тариф']
    }

    return airline


#удалить конкретную авикомпанию по её названию
def delete_airline(airline_name: str) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='DELETE FROM `Авиакомпания` WHERE `Название авиакомпании`=%s',
        sql_params=(airline_name,)
    )

    del db_con


# добавить аивикомпанию
def add_airline(airline_name) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='INSERT INTO `Авиакомпания` (`Название авиакомпании`) VALUES (%s)',
        sql_params=(airline_name,)
    )

    del db_con


#обновить данные авикомпании 
def update_airline(airline_old_name: str, airline_new_name: str) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Авиакомпания` SET `Название авиакомпании`=%s WHERE `Название авиакомпании`=%s',
        sql_params=(airline_new_name, airline_old_name)
    )

    del db_con