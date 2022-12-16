import awswrangler as wr


################################################################################################
# MOVE DATA FROM S3 TO REDSHIFT
#################################################################################################

def read_from_s3_and_insert_redshift(bucket_name,filename,glue_connection,table_name):
    s3_path=f"s3://{bucket_name}/{filename}"
    s3_data = wr.s3.read_parquet(path=s3_path)

    # # drop columns with NaN. redshift does not allow data witn NaN
    # s3_data = s3_data.drop(["payment_type","trip_type","congestion_surcharge","ehail_fee","store_and_fwd_flag",
    # "RatecodeID","PULocationID","DOLocationID","passenger_count"], axis=1)

    conn = wr.redshift.connect(glue_connection)
    wr.redshift.to_sql(
        df=s3_data,
        table=table_name,
        schema="public",
        con=conn
    )
    conn.close()

    return 


################################################################################################
# MOVE DATA FROM REDSHIFT TO S3
#################################################################################################
def move_data_from_redshift_to_s3(bucket_name,s3_filename,glue_connection,table_name):
    conn = wr.redshift.connect(glue_connection)
    wr.redshift.unload(
        sql=f"SELECT * FROM public.{table_name}",
        con=conn,
        #iam_role=iam_role,
        path=f"s3://{bucket_name}/{s3_filename}",
        keep_files=True,
    )
    conn.close()

    return
