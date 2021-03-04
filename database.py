
from __future__ import print_function
import sqlite3
from sqlite3 import connect
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = connect(db_file)
        print("CONECTADO")
    except Error as e:
        print(e)

    return conn
# # Replace username with your own A2 Hosting account username:
# conn = connect(r'./databases/test.db')
# curs = conn.cursor()
# hola =4;
# #curs.execute("CREATE TABLE employees (firstname varchar(32), lastname varchar(32), title varchar(32));")
# curs.execute("INSERT INTO employees VALUES hola)
# conn.commit()

# curs.execute("SELECT firstname, lastname FROM employees;")
# for firstname, lastname in curs.fetchall():
#     print(firstname, lastname)

# conn.close()