import sqlite3
import os
import pandas as pd

# CONSTANTS
DATABASE = r"../db/test.db"
GDP_TABLE = r"GDP"
COUNTRIES_TABLE = r"COUNTRIES"
INFLATION_TABLE = r"INFLATION"
UNEMPLOYMENT_TABLE= r"UNEMPLOYMENT"
EXCEL_FILE = r"./data/gdp/gdp_data_complete.xlsx"
COUNTRIES_SHEET_NAME = r"countries n ids"
GDP_DATA_SHEET_NAME = r"data w null"
EXCEL_FILE_V2 = r"./data/gdp/gdp_data_complete_v2.xlsx"
INCOME_LEVEL_SHEET_NAME = r"data shift w null"

def open_excel_as_dataframe(excel_file, sheet_name):
    df = None
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        return df
    except os.error as e:
        print(e)
    
    return df

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except os.error as e:
        print(e)

    return conn

def write_to_countries_table():
    try: 
        conn = create_connection(DATABASE)
        countries = open_excel_as_dataframe(EXCEL_FILE,
                                    COUNTRIES_SHEET_NAME)
        income_df = open_excel_as_dataframe(EXCEL_FILE_V2,
                                    INCOME_LEVEL_SHEET_NAME)

        with conn:
            for index, country in countries.iterrows():
                temp_df = income_df[income_df['Country'] == country['Country']]
                income = temp_df['IncomeLevel'].iloc[0]

                country_details = (country['CountryID'],
                                   country['Country'],
                                   income)
                sql = ''' INSERT INTO COUNTRIES(
                        country_id,
                        country_name,
                        income_level)
                VALUES(?,?,?) '''
                cur = conn.cursor()
                cur.execute(sql, country_details)
                conn.commit()
                print(cur.lastrowid)
    except os.error as e:
        print(e)

def write_to_gdp_table():
    try: 
        conn = create_connection(DATABASE)
        data = open_excel_as_dataframe(EXCEL_FILE,
                                    GDP_DATA_SHEET_NAME)
        income_df = open_excel_as_dataframe(EXCEL_FILE_V2,
                                    INCOME_LEVEL_SHEET_NAME)

        with conn:
            for index, row in data.iterrows():
                temp_df = income_df[income_df['Country'] == row['Country']]
                income = temp_df['IncomeLevel'].iloc[0]

                row_details = (row['CountryID'],
                               row['Country'],
                               row['Year'],
                               income,
                               row['GDP'])
                sql = ''' INSERT INTO GDP(country_id,
                                          country_name,
                                          year_,
                                          income_level,
                                          gdp_actual)
                VALUES(?,?,?,?,?) '''
                cur = conn.cursor()
                cur.execute(sql, row_details)
                conn.commit()
                print(cur.lastrowid)
    except os.error as e:
        print(e)

def write_to_inflation_table():
    try: 
        conn = create_connection(DATABASE)
        data = open_excel_as_dataframe(EXCEL_FILE,
                                    GDP_DATA_SHEET_NAME)
        income_df = open_excel_as_dataframe(EXCEL_FILE_V2,
                                    INCOME_LEVEL_SHEET_NAME)

        with conn:
            for index, row in data.iterrows():
                temp_df = income_df[income_df['Country'] == row['Country']]
                income = temp_df['IncomeLevel'].iloc[0]

                row_details = (row['CountryID'],
                               row['Country'],
                               row['Year'],
                               income,
                               row['Inflation'])
                sql = ''' INSERT INTO INFLATION(country_id,
                                          country_name,
                                          year_,
                                          income_level,
                                          inflation_actual)
                VALUES(?,?,?,?,?) '''
                cur = conn.cursor()
                cur.execute(sql, row_details)
                conn.commit()
                print(cur.lastrowid)
    except os.error as e:
        print(e)

def write_to_unemployment_table():
    try: 
        conn = create_connection(DATABASE)
        data = open_excel_as_dataframe(EXCEL_FILE,
                                    GDP_DATA_SHEET_NAME)
        income_df = open_excel_as_dataframe(EXCEL_FILE_V2,
                                    INCOME_LEVEL_SHEET_NAME)

        with conn:
            for index, row in data.iterrows():
                temp_df = income_df[income_df['Country'] == row['Country']]
                income = temp_df['IncomeLevel'].iloc[0]

                row_details = (row['CountryID'],
                               row['Country'],
                               row['Year'],
                               income,
                               row['Unemployment'])
                sql = ''' INSERT INTO UNEMPLOYMENT(country_id,
                                          country_name,
                                          year_,
                                          income_level,
                                          unemployment_actual)
                VALUES(?,?,?,?,?) '''
                cur = conn.cursor()
                cur.execute(sql, row_details)
                conn.commit()
                print(cur.lastrowid)
    except os.error as e:
        print(e)

def main():
    write_to_countries_table()
    write_to_gdp_table()
    write_to_inflation_table()
    write_to_unemployment_table()

if __name__ == '__main__':
    main()