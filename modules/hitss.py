import psycopg2
from config import host, user, password, db_name, port
import json
from psycopg2 import sql
import glob
import os



path = os.environ.get('PROJECT_PATH', '.')


def hits():

    files = glob.glob(f'{path}/json_file/hits/*.json')
    for filee in files:

        with open(filee, "r", encoding="utf-8") as fil:
            try:
                data = json.load(fil)
            except json.decoder.JSONDecodeError as err:
                continue

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
                        'INSERT INTO ga_hits (session_id, hit_date, hit_time, hit_number, hit_type, hit_referer, hit_page_path, event_category, event_action, event_label, event_value) VALUES {}')
                    .format(sql.SQL(',').join(map(sql.Literal, data_tuple))
                            )
                )
                cursor.execute(insert)

                print("[INFO] Data was successfully inserted")

        except Exception as ex:
            continue
            # print("[INFO] Error while working with PostgreSQL", ex)

        finally:
            # Закрытие соединения
            if connection:
                connection.close()
                print("[INFO] PostrgeSQL connection closed")



if __name__ == '__main__':
    hits()