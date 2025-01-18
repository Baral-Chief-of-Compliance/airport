from .main import DB_connection

# добавить визу
def add_visa(
    visa_validity_period: int,
    visa_type: str,
    visa_number_of_permitted_entries: int,
    visa_number: str
) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='INSERT INTO `Виза` (`Срок действия`, `Тип визы`, `Кол-во разрешенных въездов`, `Номер визы`) VALUES (%s,%s,%s,%s)',
        sql_params=(
            visa_validity_period,
            visa_type,
            visa_number_of_permitted_entries,
            visa_number
        )
    )

    del db_con

# получить визу по её номеру
def get_one_visa(visa_number: str) -> dict:
    visa: dict = {}

    db_con = DB_connection()

    sql_visa: tuple = db_con.select_fetchone(
        sql_query='SELECT * FROM `Виза` WHERE `Номер визы`=%s',
        sql_params=(visa_number,)
    )

    del db_con

    if sql_visa is not None:
        visa = {
            'visa_validity_period': sql_visa['Срок действия'],
            'visa_type': sql_visa['Тип визы'],
            'visa_number_of_permitted_entries': sql_visa['Кол-во разрешенных въездов'],
            'visa_number': sql_visa['Номер визы']
        }

    return visa