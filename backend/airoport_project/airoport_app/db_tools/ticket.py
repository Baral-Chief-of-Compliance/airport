from .main import DB_connection
import datetime



# посчитать свободные билеты
def count_free_ticket(flight_number: str) -> int:
    free_ticket_count : int = 0

    db_con = DB_connection()

    sql_count = db_con.select_fetchone(
        sql_query='SELECT COUNT(`Номер билета`) AS count FROM `Билет` WHERE `Номер полета`=%s AND `Выкуплены`=%s ',
        sql_params=(flight_number, False)
    )

    free_ticket_count = sql_count['count']

    del db_con

    return free_ticket_count

# получить все билеты
def get_all_flight_tickets(flight_number: str) ->list:
    tickets: list = []

    db_con = DB_connection()

    sql_tickets: tuple = db_con.select_fetchall(
        sql_query='SELECT * FROM `Билет` WHERE `Номер полета`=%s ORDER BY `Класс`',
        sql_params=(flight_number,)
    )

    del db_con

    for t in sql_tickets:
        tickets.append(
            {
                'ticket_class': t['Класс'],
                'not_valid_until_day': t['Ндд'],
                'not_valid_after_day': t['Ндп'],
                'luggage_availability': t['Наличие багажа'],
                'hand_luggage_availability':t['Наличие ручной клади'],
                'having_pet':t['Наличие питомца'],
                'ticket_number':t['Номер билета'],
                'ticket_price': t['Цена билета'],
                'ticket_bought_out':t['Выкуплены']
            }
        )

    return tickets

# получить билет по его номеру
def get_one_ticket(ticket_number: str) -> dict:
    ticket: dict = {}

    db_con = DB_connection()

    sql_ticket: tuple = db_con.select_fetchone(
        sql_query='SELECT * FROM `Билет` WHERE `Номер билета`=%s',
        sql_params=(ticket_number,)
    )

    del db_con

    ticket = {
        'flight_number': sql_ticket['Номер полета'],
        'ticket_class': sql_ticket['Класс'],
        'not_valid_until_day': sql_ticket['Ндд'],
        'not_valid_after_day': sql_ticket['Ндп'],
        'luggage_availability': sql_ticket['Наличие багажа'],
        'hand_luggage_availability':sql_ticket['Наличие ручной клади'],
        'having_pet':sql_ticket['Наличие питомца'],
        'ticket_number':sql_ticket['Номер билета'],
        'ticket_price': sql_ticket['Цена билета'],
        'ticket_price': sql_ticket['Цена билета'],
        'ticket_bought_out':sql_ticket['Выкуплены'],
        'tarif_code': sql_ticket['Тариф_Код тарифа']
    }

    return ticket


# добавить билет
def add_ticket(
    flight_number: str,
    ticket_class: str,
    flight_not_valid_until_day: int,
    flight_not_valid_after_day: int,
    ticket_index: int,
    flight_date_time: datetime.date,
    ticket_price: float
) -> None:

    ticket_not_valid_until: datetime.date = flight_date_time - datetime.timedelta(days=flight_not_valid_until_day) 
    ticket_not_valid_after: datetime.date = flight_date_time + datetime.timedelta(days=flight_not_valid_after_day)

    ticket_number = f'{flight_number}-{ticket_index}'
    db_con = DB_connection()
    db_con.sql_query_with_commit(
        sql_query='INSERT INTO `Билет` (`Номер полета`, `Класс`, `Ндд`, `Ндп`, `Номер билета`, `Цена билета`) VALUES (%s,%s,%s,%s,%s,%s)',
        sql_params=(
            flight_number,
            ticket_class,
            ticket_not_valid_until,
            ticket_not_valid_after,
            ticket_number,
            ticket_price
        )
    )
    del db_con


# обновить информацию о билете после покупки
def update_ticket_infor_after_purchase(
    ticket_number: str,
    tarif_code: str,
    luggage_availability: bool,
    hand_luggage_availability: bool,
    having_pet: bool,
) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Билет` SET `Наличие багажа`=%s, `Наличие ручной клади`=%s, `Наличие питомца`=%s, `Тариф_Код тарифа`=%s, `Выкуплены`=%s WHERE `Номер билета`=%s',
        sql_params=(
            luggage_availability, 
            hand_luggage_availability,
            having_pet,
            tarif_code,
            True,
            ticket_number
        )
    )

    del db_con


# сдать билет
def pass_ticket(
    ticket_number: str,  
) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Билет` SET `Выкуплены`=%s WHERE `Номер билета`=%s',
        sql_params=(
            False,
            ticket_number
        )
    )

    purchase =  get_purchase_by_ticket_number(ticket_number)
    
    cancel_purchase(purchase)

    del db_con

from .purchase import get_purchase_by_ticket_number, cancel_purchase