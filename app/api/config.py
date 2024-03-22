from flask_httpauth import HTTPBasicAuth
from app.user import get_user
from werkzeug.security import generate_password_hash,check_password_hash
from  app.models import create_database_connection
import secrets

auth = HTTPBasicAuth()


def generate_verify_token():
    return secrets.token_hex(32)












@auth.verify_password
def verify_password(email,password):
    user= get_user(email)
    if user and check_password_hash(user[4], password):
        return user



def create_leads(first_name=None, last_name=None, email=None, phone=None, gender=None, lead_status="lead", state=None):
    query = """
        INSERT INTO contacts
        (first_name, last_name, state_address, email_address, phone_number, gender, lead_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, state, email, phone,gender, lead_status)

    try:

        database_connection = create_database_connection()
        cursor = None
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def create_submissions(contact_id,source):
    query="""INSERT INTO form_submissions
           (contact_id,submission_source)
           VALUES (%s,%s)
    """
    values = (contact_id,source)
    try:
        database_connection = create_database_connection()
        cursor = None
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            return cursor.lastrowid

    except Exception as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()



def add_submission_data(submission_id, field_name, field_value):
    query = """INSERT INTO form_data
               (submission_id, field_name, field_value)
               VALUES (%s, %s, %s)
           """  # Add another %s for the third value
    values = (submission_id, field_name, field_value)
    try:
        database_connection = create_database_connection()
        cursor = None
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()







def normalize_key(key):
    return key.strip().replace(' ', '_').lower()






def create_standardized_model(raw_data):
    normalized_data = {}
    for key, value in raw_data.items():
        normalized_data[normalize_key(key)]=value

    required_contact_details= {'first_name', 'last_name', 'email', 'phone_number', 'gender', 'state'}
    standardized_model = {
        "first_name": None,
        "last_name": None,
        "email": None,
        "phone_number": None,
        "gender": None,
        "state": None,
        "source":"wordpress",
        "form_data":{}
    }

    for key, value in normalized_data.items():
        if key in required_contact_details:
            standardized_model[key] = value
        else:
            standardized_model["form_data"][key] = value

    return standardized_model



