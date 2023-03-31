import psycopg2
from config import host, user, password, db_name, port
import json
from psycopg2 import sql
import glob
import os


path = os.environ.get('PROJECT_PATH', '.')


def session():

    files = glob.glob(f'{path}/json_file/sessions/*.json')
    for filee in files:

        with open(filee, "r", encoding="utf-8") as fil:
            data = json.load(fil)
        dic = data[list(data.keys())[0]]

        data_tuple = [
            tuple(d.values()) + (float('NaN'),)*(len(max(data, key=len)) - len(d))
            for d in dic
        ]

        try:
            # Подключимся к БД
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port
            )
            connection.autocommit = True
            # Создадим оператор для работы с SQL
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT version();"
                )

                print(f"Server version: {cursor.fetchone()}")

            with connection.cursor() as cursor:

                insert = (
                    sql.SQL(
                        'INSERT INTO ga_sessions (session_id, client_id, visit_date, visit_time, visit_number, utm_source, utm_medium, utm_campaign, utm_adcontent, utm_keyword, device_category, device_os, device_brand, device_model, device_screen_resolution, device_browser, geo_country, geo_city) VALUES {}')
                    .format(sql.SQL(',').join(map(sql.Literal, data_tuple))
                            )
                )
                cursor.execute(insert)

                print("[INFO] Data was successfully inserted")

        except Exception as ex:
            print("[INFO] Error while working with PostgreSQL", ex)
        finally:
            # Закрытие соединения
            if connection:
                connection.close()
                print("[INFO] PostrgeSQL connection closed")



if __name__ == '__main__':
    session()