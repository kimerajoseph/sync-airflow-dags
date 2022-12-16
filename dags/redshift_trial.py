"""
This is an example dag for using `RedshiftSQLOperator` to authenticate with Amazon Redshift
then execute a simple select statement
"""
from datetime import datetime

# [START redshift_operator_howto_guide]
from airflow import DAG
from airflow.providers.amazon.aws.operators.redshift import RedshiftSQLOperator

with DAG(dag_id="redshift", start_date=datetime(2021, 1, 1), catchup=False,
    schedule_interval=None, tags=['testing-dags']) as dag:
    # [START howto_operator_redshift_create_table]
    setup__task_create_table = RedshiftSQLOperator(
        task_id='setup_create_table',
        sql="""
            CREATE TABLE IF NOT EXISTS fruit (
            fruit_id INTEGER,
            name VARCHAR NOT NULL,
            color VARCHAR NOT NULL
            );
        """,
    )
    # [END howto_operator_redshift_create_table]
    # [START howto_operator_redshift_populate_table]
    task_insert_data = RedshiftSQLOperator(
        task_id='task_insert_data',
        sql=[
            "INSERT INTO fruit VALUES ( 1, 'Banana', 'Yellow');",
            "INSERT INTO fruit VALUES ( 2, 'Apple', 'Red');",
            "INSERT INTO fruit VALUES ( 3, 'Lemon', 'Yellow');",
            "INSERT INTO fruit VALUES ( 4, 'Grape', 'Purple');",
            "INSERT INTO fruit VALUES ( 5, 'Pear', 'Green');",
            "INSERT INTO fruit VALUES ( 6, 'Strawberry', 'Red');",
        ],
    )
    # [END howto_operator_redshift_populate_table]
    # [START howto_operator_redshift_get_all_rows]
    task_get_all_table_data = RedshiftSQLOperator(
        task_id='task_get_all_table_data', sql="CREATE TABLE more_fruit AS SELECT * FROM fruit;"
    )
    # [END howto_operator_redshift_get_all_rows]
    # [START howto_operator_redshift_get_with_filter]
    task_get_with_filter = RedshiftSQLOperator(
        task_id='task_get_with_filter',
        sql="CREATE TABLE filtered_fruit AS SELECT * FROM fruit WHERE color = '{{ params.color }}';",
        params={'color': 'Red'},
    )
    # [END howto_operator_redshift_get_with_filter]

    setup__task_create_table >> task_insert_data >> task_get_all_table_data >> task_get_with_filter
# [END redshift_operator_howto_guide]