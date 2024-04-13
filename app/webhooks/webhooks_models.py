from flask_httpauth import HTTPBasicAuth
from app.users.admin_models import get_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.database import create_database_connection
import secrets
import re
from datetime import datetime


auth = HTTPBasicAuth()

patterns = {
    "non_english": re.compile(r'[^\x00-\x7F]+'),  # Matches any non-ASCII character, common in non-English text.
    "large_numbers": re.compile(r'\b\d{5,}\b'),  # Matches any number with five or more digits.
}


def generate_verify_token():
    return secrets.token_hex(16)


@auth.verify_password
def verify_password(email, password):
    user = get_user(email)
    if user and check_password_hash(user[4], password):
        return user


def create_new_leads(first_name=None, last_name=None, email=None, phone=None, gender=None, lead_status="lead",
                     state=None):
    query = """
        INSERT INTO contacts
        (first_name, last_name, state_address, email_address, phone_number, gender, lead_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, state, email, phone, gender, lead_status)
    database_connection = None
    cursor = None

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


def create_new_form_submission(contact_id, source):
    query = """INSERT INTO form_submissions
           (contact_id,submission_source)
           VALUES (%s,%s)
    """
    values = (contact_id, source)
    database_connection = None
    cursor = None
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


def add_new_form_submission_data(submission_id, field_name, field_value):
    query = """INSERT INTO form_data
               (submission_id, field_name, field_value)
               VALUES (%s, %s, %s)
           """  # Add another %s for the third value
    values = (submission_id, field_name, field_value)
    database_connection = None
    cursor = None
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


def standardized_model_wordpress(raw_data):
    normalized_data = {}
    for key, value in raw_data.items():
        normalized_data[normalize_key(key)] = value
    required_contact_details = {'first_name', 'last_name', 'email', 'phone_number', 'gender', 'state'}
    standardized_model = {
        "first_name": None,
        "last_name": None,
        "email": None,
        "phone_number": None,
        "gender": None,
        "state": None,
        "form_data": {}
    }
    for key, value in normalized_data.items():
        if key in required_contact_details:
            standardized_model[key] = value
        else:
            standardized_model["form_data"][key] = value
    return standardized_model


def standardized_model_facebook(raw_data):
    standardized_model = {
        'first_name': None,
        'last_name': None,
        'email': None,
        'phone_number': None,
        'gender': None,
        'state': None,
        'form_data': {}
    }
    normalized_data = {normalize_key(key): value for key, value in raw_data.items()}
    for key, value in normalized_data.items():
        if key in standardized_model:
            standardized_model[key] = value
        else:
            standardized_model['form_data'][key] = value
    return standardized_model


def is_invalid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return True
    return False


def has_unrealistic_numbers(submission):
    max_days = 365 * 10  # Example: 10 years in days
    max_people = 1000
    if int(submission.get('Number Of Days', 0)) > max_days or int(submission.get('Number Of People', 0)) > max_people:
        return True
    return False


def contains_spam_content(submission):
    spam_keywords = ['прокат квадроциклов', 'Круизы', 'Ещё можно узнать', 'Эко-туризм']
    spam_domains = ['mailcos.site', 'samoylovaoxana.ru']
    message = submission.get('Message', '').lower()
    email = submission.get('Email', '').lower()
    if any(keyword in message for keyword in spam_keywords):
        return True
    if any(domain in email for domain in spam_domains):
        return True
    return False


def is_gibberish_name(name):
    if len(name) < 3 or not re.search("[aeiou]", name.lower()):
        return True
    return False


def is_spam(submission):
    if is_invalid_date(submission.get('From Date', '')) or is_invalid_date(submission.get('To Date', '')):
        return True
    if has_unrealistic_numbers(submission):
        return True
    if contains_spam_content(submission):
        return True
    if is_gibberish_name(submission.get('First Name', '')) or is_gibberish_name(submission.get('Last Name', '')):
        return True
    return False



