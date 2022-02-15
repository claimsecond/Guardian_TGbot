from pprint import isreadable
import sqlite3
from sqlite3 import Error
import settings

def ensure_connection(func):
    '''Декортаор подключения к БД. 
    открывает соединение, выполняет переданную функцию, закрывает соединение
    DB_NAME указывается в файле settings.py
    Взято отсюда https://bitbucket.org/vkasatkin/tele_bot/src/master/archive_bot/db.py'''

    def inner(*args, **kwargs):
        with sqlite3.connect(settings.DB_NAME) as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner

@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS users')

    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
    ID             INTEGER PRIMARY KEY AUTOINCREMENT
                           NOT NULL,
    userid         INT     NOT NULL,
    dcv_zone       STRING  DEFAULT NULL,
    zone_selected  STRING  DEFAULT NULL,
    dcv_auto_type  STRING  DEFAULT NULL,
    type_selected  STRING  DEFAULT NULL,
    dcv_suminsured STRING  DEFAULT NULL
    );
    ''')
    # сохранить изменения
    conn.commit()


@ensure_connection
def check_user_exists(conn, user_id: int):
    '''check if user exists in db, if not - write user id into the db'''
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE userid = ?', (user_id,))
    if c.fetchone() == None:
        # если пользователь с таким ID не найден, создаем запись в БД для данного ID
        try: 
            c.execute('INSERT INTO users(userid) VALUES (?)', (user_id,))
        except Error as e:
            print(e)
    # проверяем что пользователь создан, если создан - возвращаем его ID
    c.execute('SELECT * FROM users WHERE userid = ?', (user_id,))
    data = c.fetchone()[1]
            
    conn.commit()
    return data


@ensure_connection
def get_user_state(conn, user_id: int, col: str):
    '''gets state for selected col'''
    if check_user_exists(user_id=user_id) != None: 
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE userid = ?', (user_id,))
        data = c.fetchone()[col]
        return data


@ensure_connection
def set_user_state(conn, user_id: int, col: str, state: str):
    if check_user_exists(user_id=user_id) != None: 
        c = conn.cursor()
        try: 
            c.execute(f'UPDATE users SET {col} = ? WHERE userid = ?', (state, user_id))
        except Error as e:
            print(e)

@ensure_connection
def delete_user(conn, user_id: int):
    if check_user_exists(user_id=user_id) != None: 
        c = conn.cursor()
        try: 
            c.execute(f'DELETE FROM users WHERE userid = ?', (user_id,))
        except Error as e:
            print(e)



    

   