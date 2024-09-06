import psycopg2
from psycopg2 import OperationalError

DB_PARAMS = {
    'dbname': 'telecom',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': '5432'
}

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(**DB_PARAMS)
    return conn

def query_db(query, params=None):
    """Execute a query and return the results."""
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()
    conn.close()
    return result

def execute_db(query, params=None):
    """Execute a query that does not return results (e.g., INSERT, UPDATE)."""
    conn = connect_to_db()
    with conn.cursor() as cursor:
        cursor.execute(query, params)
    conn.commit()
    conn.close()

def test_connection():
    """Test the database connection."""
    try:
        conn = connect_to_db()
        print("Connection successful")
        conn.close()
    except OperationalError as e:
        print(f"Error: {e}")

# Test the connection
test_connection()
