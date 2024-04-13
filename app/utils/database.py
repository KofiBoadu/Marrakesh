import logging
import os
from urllib.parse import urlparse
import mysql.connector
from dotenv import load_dotenv


load_dotenv()



def create_database_connection():
    """
        Establishes a database connection using the connection string from environment variables.

        Returns:
        - A database connection object if successful, None otherwise.

        Raises:
        - ValueError: If the DATABASE_URL environment variable is not set.
        - Logs an error message if the connection fails for any other reason.
    """
    database_url = os.getenv('JAWSDB_URL')
    if database_url:
        parsed_url = urlparse(database_url)
        db_user = parsed_url.username
        db_password = parsed_url.password
        db_host = parsed_url.hostname
        db_name = parsed_url.path.lstrip('/')
        db_port = parsed_url.port
        try:
            sql_connection = mysql.connector.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                database=db_name,
                port=db_port
            )
            return sql_connection

        except mysql.connector.Error as e:
            logging.error(f"An error occurred while connecting to the database: {e}")

    else:
        logging.error("DATABASE_URL not set")
        raise ValueError("DATABASE_URL not set")