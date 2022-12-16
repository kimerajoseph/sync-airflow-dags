from datetime import datetime
from airflow.utils.dates import days_ago

from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

default_args = {
    "owner": "kimera",
    "depends_on_past": False,
    'email_on_failure': False,
    'email_on_retry': False,
    "retries": 1,
    "start_date": days_ago(2),
    
}


def test_environ():
    # print("BUCKET FROM ENV IS: ", bucket_name)
    logging.info("DAG TEST SUCCESSFUL")


def test_params():
    new_age = 30
    return new_age
    

with DAG(
    dag_id="test_env_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['testing-dags'],
) as dag:

    test_environment_vars = PythonOperator(
        task_id="test_environment_vars",
        python_callable=test_environ,

    )

    test_passing_params = PythonOperator(
        task_id="test_passing_params",
        python_callable=test_params,
    )

    test_environment_vars >> test_passing_params