import pandas as pd
import psycopg2
# Using psycopg2
def load_data(db_params, query):
    connection = psycopg2.connect(
        dbname=db_params['dbname'],
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port']
    )
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df