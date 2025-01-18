from .main import DB_connection
import secrets


# получить все тарифы
def get_all_tarifs() -> list:
    tarifs: list = []

    db_con = DB_connection()

    sql_tarifs: tuple = db_con.select_fetchall(
        sql_query='SELECT * FROM `Тариф`'
    )

    del db_con

    for t in sql_tarifs:
        tarifs.append(
            {
                'name': t['Название тарифа'],
                'permissible_luggage_weight': t['Допустимый вес багажа'],
                'permissible_weight_hand_luggage': t['Допустимый вес ручной клади'],
                'extra_fee_for_pet': t['Доп.плата за питомца'],
                'possibility_of_changing_ticket': t['Возможность изменения билета'],
                'choice_of_location': t['Выбор места'],
                'possibility_of_return': t['Возможность возврата'],
                'number_of_accrued_bonuses': t['Кол-во начисления бонусов'],
                'possibility_of_upgrade': t['Возможность повышения класса'],
                'availability_of_open_departure_date': t['Наличие открытой даты вылета'],
                'priority_registration': t['Приоритетная регистрация'],
                'priority_screening': t['Приоритетный досмотр'],
                'priority_boarding': t['Приоритетная посадка'],
                'priority_baggage_handling': t['Приоритетное обслуживание багажа'],
                'tarif_code': t['Код тарифа'],
                'airline_name': t['Авиакомпания_Название авиакомпании']
            }
        )
    
    return tarifs


#получить все тарифы конкертной авикомпании
def get_all_tarifs_from_airline(airline:  str) -> list:
    tarifs: list = []

    db_con = DB_connection()

    sql_tarifs: tuple = db_con.select_fetchall(
        sql_query='SELECT * FROM `Тариф` WHERE `Авиакомпания_Название авиакомпании`=%s',
        sql_params=(airline,)
    )

    del db_con

    for t in sql_tarifs:
        tarifs.append(
            {
                'name': t['Название тарифа'],
                'permissible_luggage_weight': t['Допустимый вес багажа'],
                'permissible_weight_hand_luggage': t['Допустимый вес ручной клади'],
                'extra_fee_for_pet': t['Доп.плата за питомца'],
                'possibility_of_changing_ticket': t['Возможность изменения билета'],
                'choice_of_location': t['Выбор места'],
                'possibility_of_return': t['Возможность возврата'],
                'number_of_accrued_bonuses': t['Кол-во начисления бонусов'],
                'possibility_of_upgrade': t['Возможность повышения класса'],
                'availability_of_open_departure_date': t['Наличие открытой даты вылета'],
                'priority_registration': t['Приоритетная регистрация'],
                'priority_screening': t['Приоритетный досмотр'],
                'priority_boarding': t['Приоритетная посадка'],
                'priority_baggage_handling': t['Приоритетное обслуживание багажа'],
                'tarif_code': t['Код тарифа'],
                'airline_name': t['Авиакомпания_Название авиакомпании']
            }
        )
    
    return tarifs


# получить конкретный тариф по его номеру
def get_one_tarif(tarif_code: str) -> dict:
    tarif: dict = {}

    db_con = DB_connection()

    sql_tarif: tuple = db_con.select_fetchone(
        sql_query='SELECT * FROM `Тариф` WHERE `Код тарифа`=%s',
        sql_params=(tarif_code,)
    )

    del db_con

    tarif = {
        'name': sql_tarif['Название тарифа'],
        'permissible_luggage_weight': sql_tarif['Допустимый вес багажа'],
        'permissible_weight_hand_luggage': sql_tarif['Допустимый вес ручной клади'],
        'extra_fee_for_pet': sql_tarif['Доп.плата за питомца'],
        'possibility_of_changing_ticket': sql_tarif['Возможность изменения билета'],
        'choice_of_location': sql_tarif['Выбор места'],
        'possibility_of_return': sql_tarif['Возможность возврата'],
        'number_of_accrued_bonuses': sql_tarif['Кол-во начисления бонусов'],
        'possibility_of_upgrade': sql_tarif['Возможность повышения класса'],
        'availability_of_open_departure_date': sql_tarif['Наличие открытой даты вылета'],
        'priority_registration': sql_tarif['Приоритетная регистрация'],
        'priority_screening': sql_tarif['Приоритетный досмотр'],
        'priority_boarding': sql_tarif['Приоритетная посадка'],
        'priority_baggage_handling': sql_tarif['Приоритетное обслуживание багажа'],
        'tarif_code': sql_tarif['Код тарифа'],
        'airline_name': sql_tarif['Авиакомпания_Название авиакомпании']
        }

    return tarif


# удалить конкретный тариф
def delete_tarif(tarif_code: str) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='DELETE FROM `Тариф` WHERE `Код тарифа`=%s',
        sql_params=(tarif_code,)
    )

    del db_con


# добавить тариф
def add_tarif(
    name: str,
    permissible_luggage_weight: float,
    permissible_weight_hand_luggage: float,
    extra_fee_for_pet: bool,
    possibility_of_changing_ticket: bool,
    choice_of_location: bool,
    possibility_of_return: bool,
    number_of_accrued_bonuses: int,
    possibility_of_upgrade: bool,
    availability_of_open_departure_date: bool,
    priority_registration: bool,
    priority_screening: bool,
    priority_boarding: bool,
    priority_baggage_handling: bool,
    airline_name: str
) -> None:
    tarif_code = secrets.token_hex(16)

    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='''
        INSERT INTO `Тариф` 
        (`Название тарифа`, `Допустимый вес багажа`,`Допустимый вес ручной клади`, `Доп.плата за питомца`, 
        `Возможность изменения билета`, `Выбор места`, `Возможность возврата`,
        `Кол-во начисления бонусов`, `Возможность повышения класса`, `Наличие открытой даты вылета`,
        `Приоритетная регистрация`, `Приоритетный досмотр`, `Приоритетная посадка`,
        `Приоритетное обслуживание багажа`, `Код тарифа`, `Авиакомпания_Название авиакомпании`
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''',
        sql_params=(
                name,
                permissible_luggage_weight,
                permissible_weight_hand_luggage,
                extra_fee_for_pet,
                possibility_of_changing_ticket,
                choice_of_location,
                possibility_of_return,
                number_of_accrued_bonuses,
                possibility_of_upgrade,
                availability_of_open_departure_date,
                priority_registration,
                priority_screening,
                priority_boarding,
                priority_baggage_handling,
                tarif_code,
                airline_name
        )
    )

    del db_con


# обновление тарифа
def update_tarif(
    name: str,
    permissible_luggage_weight: float,
    permissible_weight_hand_luggage: float,
    extra_fee_for_pet: bool,
    possibility_of_changing_ticket: bool,
    choice_of_location: bool,
    possibility_of_return: bool,
    number_of_accrued_bonuses: int,
    possibility_of_upgrade: bool,
    availability_of_open_departure_date: bool,
    priority_registration: bool,
    priority_screening: bool,
    priority_boarding: bool,
    priority_baggage_handling: bool,
    tarif_code: str,
    airline_name: str      
)->None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='''
        UPDATE `Тариф` SET
        `Название тарифа`=%s, `Допустимый вес багажа`=%s,`Допустимый вес ручной клади`=%s, `Доп.плата за питомца`=%s, 
        `Возможность изменения билета`=%s, `Выбор места`=%s, `Возможность возврата`=%s,
        `Кол-во начисления бонусов`=%s, `Возможность повышения класса`=%s, `Наличие открытой даты вылета`=%s,
        `Приоритетная регистрация`=%s, `Приоритетный досмотр`=%s, `Приоритетная посадка`=%s,
        `Приоритетное обслуживание багажа`=%s, `Авиакомпания_Название авиакомпании`=%s
        WHERE `Код тарифа`=%s
        ''',
        sql_params=(
            name,
            permissible_luggage_weight,
            permissible_weight_hand_luggage,
            extra_fee_for_pet,
            possibility_of_changing_ticket,
            choice_of_location,
            possibility_of_return,
            number_of_accrued_bonuses,
            possibility_of_upgrade,
            availability_of_open_departure_date,
            priority_registration,
            priority_screening,
            priority_boarding,
            priority_baggage_handling,
            airline_name,
            tarif_code
        )
    )

    del db_con