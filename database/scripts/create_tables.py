import sqlite3
import os

# constants 
database = r"./database/test.db"

sql_create_countries_table = """ CREATE TABLE IF NOT EXISTS COUNTRIES (
                                country_id INTEGER NOT NULL PRIMARY KEY,
                                country_name TEXT NOT NULL,
                                income_level TEXT
                            ); """

sql_create_gdp_table = """ CREATE TABLE IF NOT EXISTS GDP (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        country_id INTEGER NOT NULL,
                        country_name TEXT NOT NULL,
                        year_ INTEGER NOT NULL,
                        income_level TEXT,
                        gdp_actual REAL,
                        gdp_predict REAL,
                        FOREIGN KEY (country_id) REFERENCES countries (country_id),
                        FOREIGN KEY (country_name) REFERENCES countries (country_name),
                        FOREIGN KEY (income_level) REFERENCES countries (income_level)
                    ); """

sql_create_inflation_table = """ CREATE TABLE IF NOT EXISTS INFLATION (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        country_id INTEGER NOT NULL,
                        country_name TEXT NOT NULL,
                        year_ INTEGER NOT NULL,
                        income_level TEXT,
                        inflation_actual REAL,
                        inflation_predict REAL,
                        FOREIGN KEY (country_id) REFERENCES countries (country_id),
                        FOREIGN KEY (country_name) REFERENCES countries (country_name),
                        FOREIGN KEY (income_level) REFERENCES countries (income_level)
                    ); """

sql_create_unemployment_table = """ CREATE TABLE IF NOT EXISTS UNEMPLOYMENT (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        country_id INTEGER NOT NULL,
                        country_name TEXT NOT NULL,
                        year_ INTEGER NOT NULL,
                        income_level TEXT,
                        unemployment_actual REAL,
                        unemployment_predict REAL,
                        FOREIGN KEY (country_id) REFERENCES countries (country_id),
                        FOREIGN KEY (country_name) REFERENCES countries (country_name),
                        FOREIGN KEY (income_level) REFERENCES countries (income_level)
                    ); """


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except os.error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except os.error as e:
        print(e)


def main():
    # create database connection
    conn = create_connection(database)

    if conn is not None:
        # create countries table
        create_table(conn, sql_create_countries_table)

        # create gdp table
        create_table(conn, sql_create_gdp_table)

        # create inflation table
        create_table(conn, sql_create_inflation_table)

        # create unemployment table
        create_table(conn, sql_create_unemployment_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()