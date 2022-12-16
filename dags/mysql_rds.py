# import datetime

# from airflow import DAG
# #from airflow.providers.postgres.operators.mysql import MySqlOperator
# from airflow.providers.mysql.operators.mysql import MySqlOperator

# # create_pet_table, populate_pet_table, get_all_pets, and get_birth_date are examples of tasks created by
# # instantiating the Postgres Operator

# with DAG(
#     dag_id="mysql_operator_dag",
#     start_date=datetime.datetime(2020, 2, 2),
#     schedule_interval="@once",
#     catchup=False,
#     tags=['testing-dags']
# ) as dag:
#     create_pet_table = MySqlOperator(
#     task_id="create_pet_table",
#     mysql_conn_id="mysql_default",
#     sql="sql/mysql_query.sql",
# )
