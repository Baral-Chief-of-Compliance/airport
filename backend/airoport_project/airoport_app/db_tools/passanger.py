from .main import DB_connection

# добавить пассажира
def add_passenger(
    surname_passenger: str,
    name_passenger: str,
    patronymic_passenger: str,
    phone_number_passenger: str,
    passenger_age: int,
    passport_series_passenger: int,
    passport_number_passenger: int,
    abroad_passport_series_passenger: int,
    abroad_passport_number_passenger: int,
) -> None:
    db_con = DB_connection()

    if abroad_passport_series_passenger is None and abroad_passport_number_passenger is None:
        db_con.sql_query_with_commit(
            sql_query='INSERT INTO `Пассажир` (`Фамилия`, `Имя`, `Отчество`, `Номер телефона`, `Возраст`, `Серия`, `Номер`) VALUES (%s,%s,%s,%s,%s,%s,%s)',
            sql_params=(
                surname_passenger,
                name_passenger,
                patronymic_passenger,
                phone_number_passenger,
                passenger_age,
                passport_series_passenger,
                passport_number_passenger
                )
        )
    else:

        db_con.sql_query_with_commit(
            sql_query='INSERT INTO `Пассажир` (`Фамилия`, `Имя`, `Отчество`, `Номер телефона`, `Возраст`, `Серия`, `Номер`, `Серия загран паспорта`, `Номер загран паспорта`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            sql_params=(
                surname_passenger,
                name_passenger,
                patronymic_passenger,
                phone_number_passenger,
                passenger_age,
                passport_series_passenger,
                passport_number_passenger,
                abroad_passport_series_passenger,
                abroad_passport_number_passenger
            )
        )

    del db_con


# получить пассажира по его номеру и серии паспорта
def get_one_passenger(
        passport_series_passenger: int,
        passport_number_passenger: int
        ) -> dict:
    
    passenger : dict = {}

    db_con = DB_connection()

    sql_passenger : tuple = db_con.select_fetchone(
        sql_query='SELECT * FROM `Пассажир` WHERE `Серия`=%s AND `Номер`=%s',
        sql_params=(passport_series_passenger, passport_number_passenger)
    )

    if sql_passenger is not None:
        passenger = {
            'surname_passenger':  sql_passenger['Фамилия'],
            'name_passenger':  sql_passenger['Имя'],
            'patronymic_passenger':  sql_passenger['Отчество'],
            'phone_number_passenger':  sql_passenger['Номер телефона'],
            'passenger_age':  sql_passenger['Возраст'],
            'passport_series_passenger':  sql_passenger['Серия'],
            'passport_number_passenger':  sql_passenger['Номер'],
            'abroad_passport_series_passenger':  sql_passenger['Серия загран паспорта'],
            'abroad_passport_number_passenger':  sql_passenger['Номер загран паспорта'],
        }

    del db_con

    return passenger

# обновить возраст, данные загран паспорта пассажира
def update_passenger_sensitive_data(
    passport_series_passenger: int,
    passport_number_passenger: int,
    abroad_passport_series_passenger: int,
    abroad_passport_number_passenger: int,
    new_age: int
) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Пассажир` SET `Возраст`=%s, `Серия загран паспорта`=%s, `Номер загран паспорта`=%s WHERE `Серия`=%s AND `Номер`=%s',
        sql_params=(
            new_age,
            abroad_passport_series_passenger,
            abroad_passport_number_passenger,
            passport_series_passenger, 
            passport_number_passenger
            )
    )

    del db_con