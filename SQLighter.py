import sqlite3
from sqlite3 import Error
import settings

def ensure_connection(func):
    '''Декортаор подключения к БД. 
    открывает соединение, выполняет переданную функцию, закрывает соединение
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
            ID     INTEGER PRIMARY KEY AUTOINCREMENT
                   NOT NULL,
            userid INT     NOT NULL,
            state  STRING  NOT NULL
        );
    ''')
    # сохранить изменения
    conn.commit()

@ensure_connection
def set_user_state(conn, user_id: int, state: str):
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE userid = ?', (user_id,))
    if c.fetchone() == None:
        try: 
            c.execute('INSERT INTO users(userid, state) VALUES (?,?)', (user_id, state))
        except Error as e:
            print(e)

    try: 
        c.execute('UPDATE users SET state = ? WHERE userid = ?', (state, user_id))
    except Error as e:
        print(e)
        
    conn.commit()

@ensure_connection
def get_user_state(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT state FROM users WHERE userid = ?', (user_id,))
    data = c.fetchone()
    return data
    

# @ensure_connection
# def test_DB_func(conn):
#     c = conn.cursor()
#     c.execute("SELECT state FROM users WHERE userid = {userid}".format(userid=1111111))
#     data = c.fetchone()
#     return data
    

   