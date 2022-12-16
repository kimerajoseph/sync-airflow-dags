from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
#import awswrangler as wr

from python_scripts import move_data_between_s3_and_redshift

BUCKET_NAME = Variable.get("redshift_bucket")
filename="SOE_4th_22nd_Nov_2022.parquet"
s3_filename="from_red2.parquet"
GLUE_CONNECTION = Variable.get("glue_redshift_connection")





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

with DAG(
    dag_id="move_data_from_s3_to_redshidt_with_awswrangler",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=2,
    tags=['testing-dags'],
    ) as dag:


    move_data_from_s3_to_redshift = PythonOperator(
        task_id="move_data_from_s3_to_redshift",
        python_callable=move_data_between_s3_and_redshift.read_from_s3_and_insert_redshift,
        op_kwargs={
            "bucket_name":BUCKET_NAME,
            "filename":filename,
            "glue_connection":GLUE_CONNECTION,
            "table_name":"airflow_trips"
        }
    )


    task_move_data_from_redshift_to_s3 = PythonOperator(
            task_id="move_data_from_redshift_to_s3",
        python_callable=move_data_between_s3_and_redshift.move_data_from_redshift_to_s3,
        op_kwargs={
            "bucket_name":BUCKET_NAME,
            "s3_filename":s3_filename,
            "glue_connection":GLUE_CONNECTION,
            "table_name":"airflow_trips"
        }
    )

    task_move_data_from_redshift_to_s3.set_upstream(move_data_from_s3_to_redshift)