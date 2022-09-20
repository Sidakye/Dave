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

def get_all_gdp() -> list:
    rows = None
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM GDP
                       WHERE income_level IS NOT NULL''')

        rows = cur.fetchall()

    except error as e:
        print('Failed to get all gdp from the database', e)

    close_connection(conn)
    return rows

def get_gdp_by_country_name(country_name: str) -> list:
    rows = None
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()
        query = '''SELECT * FROM GDP WHERE country_name = ?'''
        cur.execute(query, (country_name,))

        rows = cur.fetchall()
    except error as e:
        print('Failed to get country gdp from the database', e)

    close_connection(conn)
    return rows

def get_gdp_by_country_id(country_id: int) -> list:
    rows = None
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()
        query = '''SELECT * FROM GDP WHERE country_id = ?'''
        cur.execute(query, (country_id,))

        rows = cur.fetchall()

        return rows

    except error as e:
        print('Failed to get country gdp from the database', e)

    close_connection(conn)
    return rows


def get_all_countries() -> list:
    countries = None
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM COUNTRIES
                       WHERE income_level IS NOT NULL''')

        rows = cur.fetchall()

        if len(rows) > 0:
            countries = rows
        else:
            countries = None
    except error as e:
        print('Failed to get list of countries', e)

    close_connection(conn)
    return countries

def get_country_details_by_name(name: str) -> tuple:
    country = None
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()
        query = '''SELECT * FROM COUNTRIES
                       WHERE country_name = ?'''
        cur.execute(query, (name,))

        country = cur.fetchone()
    except error as e:
        print('Failed to get country details', e)

    close_connection(conn)
    return country

def insert_new_prediction(country_details: tuple, year: int, prediction: float):
    try:
        conn = create_connection(DATABASE)
        cur = conn.cursor()

        query = ''' INSERT INTO GDP(country_id, country_name,
                                    year_, income_level,
                                    gdp_predict)
                VALUES(?,?,?,?,?) '''
        data = (country_details[0], country_details[1],
                year, country_details[2], prediction)

        cur.execute(query, data)
        conn.commit()

        print(cur.lastrowid)
        close_connection(conn)
    except error as e:
        print('Failed to insert prediction into database', e)
        