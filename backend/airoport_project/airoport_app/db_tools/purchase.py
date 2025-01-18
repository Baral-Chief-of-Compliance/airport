from .main import DB_connection
import datetime
import time
import secrets


from .visa import add_visa, get_one_visa
from .passanger import add_passenger, get_one_passenger, update_passenger_sensitive_data
from .flight import  get_one_flight
from .ticket import update_ticket_infor_after_purchase, get_one_ticket

# формить покупку
def make_purchase(
    surname_passenger: str,
    name_passenger: str,
    patronymic_passenger: str,
    phone_number_passenger: str,
    passenger_age : int,
    passport_series_passenger: int,
    passport_number_passenger: int,
    abroad_passport_series_passenger: int,
    abroad_passport_number_passenger: int,
    visa_validity_period: int,
    visa_type: str,
    visa_number_of_permitted_entries: int,
    visa_number: str,
    cashier_id: int,
    tarif_code: str,
    extra_fee_for_dog: float,
    flight_number: str,
    ticket_number: str,
    luggage_availability: bool,
    hand_luggage_availability: bool,
    having_pet: bool
    ) -> None:

    db_con = DB_connection()

    #проверка на наличие поссажира
    passenger : dict = get_one_passenger(
        passport_number_passenger=passport_number_passenger,
        passport_series_passenger=passport_series_passenger
    )

    # Добавим пассажира, при условие что его нет.
    if not bool(passenger):
        add_passenger(
            surname_passenger=surname_passenger,
            name_passenger=name_passenger,
            patronymic_passenger=patronymic_passenger,
            phone_number_passenger=phone_number_passenger,
            passenger_age=passenger_age,
            passport_number_passenger=passport_number_passenger,
            passport_series_passenger=passport_series_passenger,
            abroad_passport_number_passenger=abroad_passport_number_passenger,
            abroad_passport_series_passenger=abroad_passport_series_passenger,
        )
    else:
        #проверка то, изменились ли чувствительные данные
        if passenger['passenger_age']!=passenger_age or passenger['abroad_passport_series_passenger']!=abroad_passport_series_passenger or passenger['abroad_passport_number_passenger']!=abroad_passport_number_passenger:
            update_passenger_sensitive_data(
                passport_series_passenger=passport_series_passenger,
                passport_number_passenger=passport_number_passenger,
                abroad_passport_series_passenger=abroad_passport_series_passenger,
                abroad_passport_number_passenger=abroad_passport_number_passenger,
                new_age=passenger_age
            )

    #поулчить полет 
    flight = get_one_flight(flight_number=flight_number)

    #получить билет
    ticket = get_one_ticket(ticket_number=ticket_number)

    # финальная цена
    if extra_fee_for_dog is not None:
        final_price = ticket['ticket_price'] + extra_fee_for_dog
    else:
        final_price = ticket['ticket_price']

    # добавляем визу, если перелеь междунароодный
    if flight['flight_international_status']:
        # проверка на наличие визы

        visa = get_one_visa(visa_number=visa_number)

        if not bool(visa):
            add_visa(
                visa_validity_period=visa_validity_period,\
                visa_type=visa_type,
                visa_number_of_permitted_entries=visa_number_of_permitted_entries,
                visa_number=visa_number
            )

    # сегодняшняя дата
    today = datetime.datetime.today()

    #номер покупки 
    number_purchase = secrets.token_hex(16)

    if flight['flight_international_status']:
        db_con.sql_query_with_commit(
            sql_query='INSERT INTO `Покупка` (`Номер заказа`, `Финальная цена`, `Дата заказа`, `Время заказа`, `Кассир_Номер кассира`, `Виза_Номер визы`, `Полет_Номер рейса`, `Билет_Номер билета`, `Пассажир_Серия`, `Пассажир_Номер`, `Статус покупкки`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            sql_params=(
                number_purchase,
                final_price,
                today.date(),
                today.time(),
                cashier_id,
                visa_number,
                flight_number,
                ticket_number,
                passport_series_passenger,
                passport_number_passenger,
                'Офомрлена'
            )
        )
    else:
        db_con.sql_query_with_commit(
            sql_query='INSERT INTO `Покупка` (`Номер заказа`, `Финальная цена`, `Дата заказа`, `Время заказа`, `Кассир_Номер кассира`, `Полет_Номер рейса`, `Билет_Номер билета`, `Пассажир_Серия`, `Пассажир_Номер`, `Статус покупкки`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            sql_params=(
                number_purchase,
                final_price,
                today.date(),
                today.time(),
                cashier_id,
                flight_number,
                ticket_number,
                passport_series_passenger,
                passport_number_passenger,
                'Офомрлена'
            )
        )

    # обновить параметры билета
    update_ticket_infor_after_purchase(
        ticket_number=ticket_number,
        tarif_code=tarif_code,
        luggage_availability=luggage_availability,
        hand_luggage_availability=hand_luggage_availability,
        having_pet=having_pet
    )


    del db_con

# получить покупку по номеру билета
def get_purchase_by_ticket_number(
        ticket_number: str
) -> dict:
    purchase : dict = {}

    db_con = DB_connection()

    sql_purchase = db_con.select_fetchone(
        sql_query='SELECT * FROM `Покупка` WHERE `Билет_Номер билета`=%s AND `Статус покупкки`=%s',
        sql_params=(ticket_number, 'Офомрлена')
    )

    del db_con

    if sql_purchase is not None:
        purchase = {
            'number_purchase': sql_purchase['Номер заказа'],
            'final_price': sql_purchase['Финальная цена'],
            'date': sql_purchase['Дата заказа'],
            'time': sql_purchase['Время заказа'],
            'cashier_id': sql_purchase['Кассир_Номер кассира'],
            'visa_number': sql_purchase['Виза_Номер визы'],
            'flight_number': sql_purchase['Полет_Номер рейса'],
            'ticket_number': sql_purchase['Билет_Номер билета'],
            'passenger_number': sql_purchase['Пассажир_Номер'],
            'passenger_series': sql_purchase['Пассажир_Серия'],
            'status': sql_purchase['Статус покупкки']
        }
    return purchase

# отменитьб покупку
def cancel_purchase(
    number_purchase: str
) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Покупка` SET `Статус покупкки`=%s WHERE `Номер заказа`=%s',
        sql_params=(
            'Отмена',
            number_purchase
        )
    )

    del db_con