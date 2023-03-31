# import psycopg2
# from config import host, user, password, db_name, port
# import json
# import pandas as pd
#
#
#
# path = "json_file/sessions/ga_sessions_new_2022-01-03.json"
#
# def file_json(path):
#
#     with open(path, 'r') as f:
#         try:
#             data = json.load(f)
#         except json.decoder.JSONDecodeError as err:
#             return None
#     return data
#
# def dict_pd(data):
#     dic = data[list(data.keys())[0]]
#     # name_dict = list(data[list(data.keys())[0]][0].keys())
#     # df = pd.DataFrame(dic)
#     return dic
#
#
# def conn(dic):
#     try:
#         # Подключимся к БД
#         connection = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name,
#             port=port
#         )
#         connection.autocommit = True
#         # Создадим оператор для работы с SQL
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT version();"
#             )
#
#             print(f"Server version: {cursor.fetchone()}")
#
#             # def to_sql():
#             #
#             #     df.to_sql('ga_sessions', cursor, if_exists='replace', index=False)
#
#         with connection.cursor() as cursor:
#             cursor.executemany(f"INSERT INTO ga_sessions VALUES (?, ?);", dic)
#             # cursor.execute(
#             #     f"""INSERT INTO ga_sessions ({', '.join(df_1)}) VALUES
#             #     {i.tolist()}"""
#             # )
#
#             print("[INFO] Data was successfully inserted")
#
#     except Exception as ex:
#         print("[INFO] Error while working with PostgreSQL", ex)
#     finally:
#         # Закрытие соединения
#         if connection:
#             connection.close()
#             print("[INFO] PostrgeSQL connection closed")
#
#
