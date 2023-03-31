import datetime as dt
import os, glob
import sys
from airflow.models import DAG
from airflow.operators.python import PythonOperator


path = os.path.expanduser('~/final_project')
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)


args = {
    'owner': 'final_work',
    'start_date': dt.datetime(2023, 3, 29),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': False,
}


from modules.sessions import session
from modules.hitss import hits

# schedule_interval

with DAG(
        dag_id='final_work',
        schedule_interval=None,
        # schedule_interval=timedelta(days=1),
        # schedule_interval='*/15 * * * *',
        default_args=args,
) as dag:
    session = PythonOperator(
        task_id='session',
        python_callable=session,
    )

    hits = PythonOperator(
        task_id='hits',
        python_callable=hits,
    )

    session >> hits
    # del_session = PythonOperator(
    #     task_id='del_session',
    #     python_callable=del_session,
    # )
    #
    # del_hits = PythonOperator(
    #     task_id='del_hits',
    #     python_callable=del_hits,
    # )


    #session >>  del_session >> hits >> del_hits

    # <YOUR_CODE>

