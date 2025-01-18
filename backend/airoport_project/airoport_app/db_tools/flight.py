from .main import DB_connection
import datetime
import time
import secrets




# получить все полеты
def get_all_flights() -> list:
    flights: list = []

    db_con = DB_connection()

    sql_flights: tuple = db_con.select_fetchall(
        sql_query='SELECT * FROM `Полет` ORDER BY `Дата вылета` DESC, `Время вылета` DESC'
    )

    #текущая дата и время
    now_date_time = datetime.datetime.now()


    del db_con

    for f in sql_flights:
        date_time_flight = datetime.datetime.combine(f['Дата вылета'], (datetime.datetime.min + f['Время вылета']).time())

        flight_delta_time = date_time_flight-now_date_time

        if flight_delta_time.days < 0:
            flight_status = 'gray'
        elif flight_delta_time.days < 1 and flight_delta_time.seconds//3600 < 1:
            flight_status = 'red'
        elif flight_delta_time.days < 1 and flight_delta_time.seconds//3600 < 12:
            flight_status = 'orange'
        elif flight_delta_time.days < 1 and flight_delta_time.seconds//3600 < 24:
            flight_status = 'yellow'
        else:
            flight_status = 'green'

        free_ticket_count = count_free_ticket(
            flight_number=f['Номер рейса']
        )

        flights.append(
            {
                'flight_place_departure': f['Место отправления'],
                'flight_place_destination': f['Место назначения'],
                'flight_number': f['Номер рейса'],
                'flight_date': f['Дата вылета'],
                'flight_time': f['Время вылета'],
                'flight_passengers_count': f['Кол-во пассажиров'] - free_ticket_count,
                'flight_status': flight_status,
                'flight_airline': f['Авиакомпания_Название авиакомпании'],
                'flight_cancel_status': f['Рейс отменен'],
                'free_ticket_count': free_ticket_count,
            }
        )
    return flights


#получить конкретный полет по его номеру рейса
def get_one_flight(flight_number: str) -> dict:
    flight: dict = {}

    db_con = DB_connection()

    sql_flight: tuple = db_con.select_fetchone(
        sql_query='SELECT * FROM `Полет` WHERE `Номер рейса`=%s',
        sql_params=(flight_number,)
    )

    del db_con

    date_time_flight = datetime.datetime.combine(sql_flight['Дата вылета'], (datetime.datetime.min + sql_flight['Время вылета']).time())

    now_date_time = datetime.datetime.now()
    flight_delta_time = date_time_flight-now_date_time

    if flight_delta_time.days < 0:
        flight_status = 'gray'
    elif flight_delta_time.days < 1 and flight_delta_time.seconds//3600 < 1:
        flight_status = 'red'
    elif flight_delta_time.days < 1 and flight_delta_time.seconds//3600 < 12:
        flight_status = 'orange'
    elif flight_delta_time.days < 1 and flight_delta_time.seconds//3600 < 24:
        flight_status = 'yellow'
    else:
        flight_status = 'green'

    flight = {
        'flight_place_departure': sql_flight['Место отправления'],
        'flight_place_destination': sql_flight['Место назначения'],
        'flight_number': sql_flight['Номер рейса'],
        'flight_date': sql_flight['Дата вылета'],
        'flight_time': sql_flight['Время вылета'],
        'flight_passengers_count': sql_flight['Кол-во пассажиров'],
        'flight_airline': sql_flight['Авиакомпания_Название авиакомпании'],
        'flight_international_status': sql_flight['Международный'],
        'flight_cancel_status': sql_flight['Рейс отменен'],
        'flight_status': flight_status,
        }

    return flight


# удалить конкртеный рейс
def delete_flight(flight_number: str) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='DELETE FROM `Полет` WHERE `Номер рейса`=%s',
        sql_params=(flight_number,)
    )

    del db_con


# добавить вылет
def add_flight(
        flight_airline: str,
        flight_place_departure: str,
        flight_place_destination: str,
        flight_date: datetime.date,
        flight_time: time,
        flight_passengers_count: int,
        flight_international: bool
        ) -> str:
    
    flight_number = secrets.token_hex(16)

    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='INSERT INTO `Полет` (`Авиакомпания_Название авиакомпании`, `Номер рейса`, `Дата вылета`, `Время вылета`, `Кол-во пассажиров`, `Место отправления`, `Место назначения`, `Международный`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        sql_params=(
            flight_airline,
            flight_number, 
            flight_date, 
            flight_time, 
            flight_passengers_count, 
            flight_place_departure, 
            flight_place_destination,
            flight_international
            )
    )

    del db_con

    return flight_number


# обновить данные авикомпании
def update_flight(
        flight_airline: str,
        flight_place_departure: str,
        flight_place_destination: str,
        flight_number: str,
        flight_date:  datetime.date,
        flight_time: time,
        flight_passengers_count: int
    ) -> None:

    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Полет` SET `Авиакомпания_Название авиакомпании`=%s, `Дата вылета`=%s, `Время вылета`=%s, `Кол-во пассажиров`=%s, `Место отправления`=%s, `Место назначения`=%s WHERE `Номер рейса`=%s',
        sql_params=(
            flight_airline,
            flight_date, 
            flight_time, 
            flight_passengers_count, 
            flight_number,
            flight_place_departure,
            flight_place_destination
            )
    )

    del db_con

# обновить время полета
def update_flight_time(
        flight_number: str,
        flight_date:  datetime.date,
        flight_time: time,
) -> None:
    
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Полет` SET `Дата вылета`=%s, `Время вылета`=%s WHERE `Номер рейса`=%s',
        sql_params=(
            flight_date, 
            flight_time, 
            flight_number
            )
    )

    del db_con


# отменить рейс
def cancel_flight(flight_number: str) -> None:

    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Полет` SET `Рейс отменен`=%s WHERE `Номер рейса`=%s',
        sql_params=(
            True,
            flight_number
            )
    )

    del db_con


from .ticket import count_free_ticket