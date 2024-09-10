# Function to create a table
import pandas as pd
import psycopg2

def load_data(db_params, query):
    """
    Load data from PostgreSQL using psycopg2 and return as a pandas DataFrame.
    """
    connection = psycopg2.connect(
        dbname=db_params['dbname'],
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port']
    )
    DB_PARAMS = {
    'dbname': 'telecom',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

# SQL query to execute
    query = "SELECT * FROM xdr_data;"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

def create_table(db_params, create_table_query):
    """
    Create a table in the PostgreSQL database.
    """
    connection = psycopg2.connect (
        dbname=db_params['dbname'],
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port']
    )
    
    try:
        # Create a cursor object using the connection
        cursor = connection.cursor()
        # Execute the SQL query
        cursor.execute(create_table_query)
        # Commit the transaction
        connection.commit()
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Function to insert data from DataFrame into the PostgreSQL table
def insert_data_from_df(df, db_params):
    # Establish the database connection
    connection = psycopg2.connect(
        dbname=db_params['dbname'],
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port']
    )
    
    try:
        cursor = connection.cursor()
        # Iterate through each row in the DataFrame
        for _, row in df.iterrows():
            insert_query = '''
            INSERT INTO user_scores (user_id, engagement_score, experience_score, satisfaction_score)
            VALUES (%s, %s, %s, %s)
            '''
            # Execute the insert query with the data from the DataFrame
            cursor.execute(insert_query, (
                row['MSISDN/Number'], 
                row['Engagement Score'], 
                row['Experience Score'], 
                row['Satisfaction Score']
            ))

        # Commit the changes to the database
        connection.commit()
        
    except Exception as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        print(f"An error occurred: {e}")
        
    finally:
        # Ensure that the cursor and connection are closed
        cursor.close()
        connection.close()