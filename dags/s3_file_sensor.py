# from datetime import datetime, timedelta
# from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
# from airflow import DAG
# from airflow.models import Variable

# BUCKET_NAME = Variable.get("redshift_bucket")

# default_args = {
# 'owner': 'airflow',
# 'depends_on_past': False,
# 'start_date': datetime(2018, 9, 1),
# 'email_on_failure': False,
# 'email_on_retry': False,
# 'schedule_interval': '@daily',
# 'retries': 1,
# 'retry_delay': timedelta(seconds=5),
# }


# # [START howto_sensor_s3_key_function_definition]
# def check_fn(files: list) -> bool:
#     """
#     Example of custom check: check if all files are bigger than ``20 bytes``

#     :param files: List of S3 object attributes.
#     :return: true if the criteria is met
#     """
#     #return all(f.get("Size", 0) > 20 for f in files)
#     return ("green_tripdata_2021-01.parquet" in files)

# with DAG(
#     dag_id="test_s3_file_sensor",
#     schedule_interval="@daily",
#     default_args=default_args,
#     catchup=False,
#     max_active_runs=1,
#     tags=['testing-dags'],
#     ) as dag:
 
#     sensor_key_with_function = S3KeySensor(
#         task_id="sensor_key_with_function",
#         bucket_name=BUCKET_NAME,
#         bucket_key="green_tripdata_2021-01.parquet",
#         check_fn=check_fn,
#     )

#     sensor_key_with_function