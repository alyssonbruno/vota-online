from sqlite3 import connect, OperationalError


__DATABASE_FILE = '.fake-banco.db'
__CONNECTIONS__ = {}


def get_conection(database_file: str = None):
    global __CONNECTIONS__, __DATABASE_FILE
    if database_file is None:
        database_file = __DATABASE_FILE
    if database_file not in __CONNECTIONS__.keys():
        __CONNECTIONS__[database_file] = connect(database_file)
    return __CONNECTIONS__[database_file]


def create_if_not_existe_table(table_name: str, dml: str, conn=None) -> bool:
    if conn is None:
        conn = get_conection()
    try:
        conn.execute('select 1 from {}'.format(table_name))
    except OperationalError:
        conn.execute(dml)
    else:
        return False
    return True

