from .main import DB_connection


#получить всез кассиров
def get_all_cashiers() -> list:
    cashiers: list = []

    db_con = DB_connection()

    sql_cashiers: tuple = db_con.select_fetchall(
        sql_query='SELECT * FROM `Кассир`  ORDER BY `Фамилия`'
    )

    del db_con

    for sc in sql_cashiers:
        cashiers.append(
            {
                'cashier_id': sc['Номер кассира'],
                'cashier_surname': sc['Фамилия']
            }
        )

    return cashiers


# получить всех кассиров для поля select в форме при оформление покупки
def get_all_cashiers_for_purchase_form() -> list:
    cashiers: list = []
    db_con = DB_connection()

    sql_cashiers: tuple = db_con.select_fetchall(
        sql_query='SELECT * FROM `Кассир`'
    )

    del db_con

    for c in sql_cashiers:
        cashiers.append(
            (
                c['Номер кассира'], c['Фамилия'],
            )
        )

    return cashiers


#получить конкретного кассира по его id 
def get_one_cashier(id: int) -> dict:
    cashier: dict = {}

    db_con = DB_connection()

    sql_cashier: tuple = db_con.select_fetchone(
        sql_query='SELECT * FROM `Кассир` WHERE `Номер кассира`=%s',
        sql_params=(id,)
    )

    del db_con

    cashier = {
        'cashier_id': sql_cashier['Номер кассира'],
        'cashier_surname': sql_cashier['Фамилия']
    }

    return cashier


#удалить конкретного кассира по id
def delete_cashier(id: int) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='DELETE FROM `Кассир` WHERE `Номер кассира`=%s',
        sql_params=(id,)
    )

    del db_con


# добавить кассира
def add_cashier(surname: str) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='INSERT INTO `Кассир` (`Фамилия`) VALUES (%s)',
        sql_params=(surname,)
    )

    del db_con


#обновить данные кассира
def update_cashier(id: int, surname: str) -> None:
    db_con = DB_connection()

    db_con.sql_query_with_commit(
        sql_query='UPDATE `Кассир` SET `Фамилия`=%s WHERE `Номер кассира`=%s',
        sql_params=(surname, id)
    )

    del db_con