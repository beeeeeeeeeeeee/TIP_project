from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.models import Connection
from airflow.utils import db
from airflow import settings
from airflow.models import Variable
import os
def create_warehouse_connection():
    warehouse_db_conn_id = 'my_warehouse_postgres_conn'
    warehouse_db_host = os.getenv("WAREHOUSE_POSTGRES_HOST")
    warehouse_db_port = os.getenv("WAREHOUSE_POSTGRES_PORT")
    warehouse_db_name = os.getenv("WAREHOUSE_POSTGRES_NAME")
    warehouse_db_user = os.getenv("WAREHOUSE_POSTGRES_USER")
    warehouse_db_password = os.getenv("WAREHOUSE_POSTGRES_PASSWORD")

    conn = Connection(
        conn_id=warehouse_db_conn_id,
        conn_type='postgres',
        host=warehouse_db_host,
        port=warehouse_db_port,
        schema=warehouse_db_name,
        login=warehouse_db_user,
        password=warehouse_db_password
    )

    session = settings.Session()
    session.add(conn)
    session.commit()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

dag = DAG(
    'create_warehouse_connection_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

create_connection = PythonOperator(
    task_id='create_warehouse_connection',
    python_callable=create_warehouse_connection,
    dag=dag
)
