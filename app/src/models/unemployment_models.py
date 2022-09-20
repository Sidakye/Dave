import sqlite3
from os import error

DATABASE = r"../../../database/db/test.db"

def create_connection(db_file: str):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except error as e:
        print('Failed to connect to the database', e)

    return conn

def close_connection(conn):
    try:
        conn.close()
    except error as e:
        print('Falie to close database connection', e)

def get_all_unemployment() -> list:
    rows = None
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM UNEMPLOYMENT
                       WHERE income_level IS NOT NULL''')

        rows = cur.fetchall()

    except error as e:
        print('Failed to get all inflation from the database', e)

    close_connection(conn)
    return rows

def get_unemployment_by_year(country_name: str, year: int) -> tuple:
    data = None
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()
        query = '''SELECT * FROM UNEMPLOYMENT
                   WHERE country_name = ?
                   AND year_ = ?'''
        cur.execute(query, (country_name, year,))

        data = cur.fetchone()
    except error as e:
        print('Failed to get inflation value', e)
    
    close_connection(conn)
    return data[5]