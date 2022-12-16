from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
# from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
import awswrangler as wr
from airflow.models import Variable

BUCKET_NAME = Variable.get("redshift_bucket")
#FILE_NAME= "green_tripdata_2021-01.parquet"
FILE_NAME="green_tripdata_2021-01.parquet"
# aws_access_key_id=Variable.get("aws_access_key_id")
# aws_secret_access_key=Variable.get("aws_access_key_value")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 2, 22),
    'email': ['nic@enye.tech'],
    'email_on_failure': False,
    'max_active_runs': 1,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5)
}

def read_data():
    s3_data = wr.s3.read_parquet(path=f"s3://{BUCKET_NAME}/{FILE_NAME}")
    #s3_data = wr.s3.read_parquet(path="s3://airflow-jkimera-bucket/green_tripdata_2021-01.parquet")
    return s3_data.shape



with DAG(
    dag_id="testing_aws_wrangler",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['testing-dags'],
    ) as dag:

    test_data_read = PythonOperator(
        task_id="read_data_with_awswrangler",
        python_callable=read_data
    )

    test_data_read