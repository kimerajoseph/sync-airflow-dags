# airflow related
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
#from airflow.operators.bash_operator import BashOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
# other packages
from datetime import datetime
from datetime import timedelta

#Airflow Read File from S3
import os
...


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 9, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'schedule_interval': '@daily',
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}


# def download_from_s3(key: str, bucket_name: str, local_path: str):
#     hook = S3Hook('s3_conn')
#     file_name = hook.download_file(key=key, bucket_name=bucket_name, local_path=local_path)
#     return file_name

def download_from_s3(key: str, bucket_name: str, local_path: str) -> str:
    hook = S3Hook('s3_conn')
    file_name = hook.download_file(key=key, bucket_name=bucket_name, local_path=local_path)
    return file_name

def rename_file(ti, new_name: str) -> None:
    downloaded_file_name = ti.xcom_pull(task_ids=['download_from_s3'])
    downloaded_file_path = '/'.join(downloaded_file_name[0].split('/')[:-1])
    os.rename(src=downloaded_file_name[0], dst=f"{downloaded_file_path}/{new_name}") 

with DAG(
    dag_id="test_s3_hook",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['testing-dags'],
    ) as dag:
    # Download a file
    task_download_from_s3 = PythonOperator(
        task_id='download_from_s3',
        python_callable=download_from_s3,
        op_kwargs={
            'key': 'green_tripdata_2021-01.parquet',
            'bucket_name': 'airflow-jkimera-bucket',
            'local_path': '/home/ec2-user/airflow/data/'
        }
    )
    #Airflow Read File from S3

     # Rename the file
    task_rename_file = PythonOperator(
        task_id='task_rename_file',
        python_callable=rename_file,
        op_kwargs={
            'new_name': 'green_tripdata.parquet'
        }
    )

    task_download_from_s3 >> task_rename_file