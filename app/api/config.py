from flask_httpauth import HTTPBasicAuth
from app.user import get_user
from werkzeug.security import generate_password_hash,check_password_hash
from  app.models import create_databaseConnection


auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(email,password):
    user= get_user(email)
    if user and check_password_hash(user[4], password):
        return user



def create_leads(first_name, last_name, email, phone, gender ,lead_status="lead",state=None):
    query = """
        INSERT INTO customers
        (first_name, last_name, state_address, email_address, phone_number, gender,lead_status)
        VALUES (%s, %s, %s, %s, %s, %s,%s)
    """
    values = (first_name, last_name, state, email, phone, gender,lead_status)

    try:
        database_connection = create_databaseConnection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

