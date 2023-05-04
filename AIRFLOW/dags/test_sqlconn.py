from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

dag = DAG(
    'test_sqlconn',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False
)

def execute_query(ds, **kwargs):
    hook = MySqlHook(mysql_conn_id='my_webdb_mysql_conn')
    connection = hook.get_conn()
    cursor = connection.cursor()
    cursor.execute("USE test")

    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='dbName'
    """)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    print(result)
    return result

run_query = PythonOperator(
    task_id='run_query',
    provide_context=True,
    python_callable=execute_query,
    dag=dag
)
