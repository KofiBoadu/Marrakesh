from flask_httpauth import HTTPBasicAuth
from app.user import get_user
from werkzeug.security import generate_password_hash,check_password_hash
from  app.models import create_database_connection
import secrets
import re

auth = HTTPBasicAuth()


patterns = {
    "non_english": re.compile(r'[^\x00-\x7F]+'),  # Matches any non-ASCII character, common in non-English text.
    "large_numbers": re.compile(r'\b\d{5,}\b'),  # Matches any number with five or more digits.
}









def generate_verify_token():
    return secrets.token_hex(16)






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






def standardized_model_wordpress(raw_data):
    normalized_data = {}
    for key,value in raw_data.items():
        normalized_data[normalize_key(key)]=value
    required_contact_details= {'first_name', 'last_name', 'email', 'phone_number', 'gender', 'state'}
    standardized_model = {
        "first_name": None,
        "last_name": None,
        "email": None,
        "phone_number": None,
        "gender": None,
        "state": None,
        "form_data":{}
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




def is_spam(request_data):

    for field in ['first_name', 'last_name', 'message']:
        if patterns['non_english'].search(request_data.get(field, '')):
            return True

    for field in ['number_of_days', 'number_of_people', 'budget']:
        value = request_data.get(field, '0').replace(' ', '')
        if patterns['large_numbers'].search(value):
            return True

    from_date = request_data.get('from_date', '')
    to_date = request_data.get('to_date', '')
    if from_date > to_date:
        return True

    return False









# # Sample raw data passed to the function
# raw_data =  {'Are you prepared to secure your spot with a deposit within the next week?': 'No', 'Are you ready to join one of our exclusive, limited-spot group trips in the next 3 months?': 'Maybe, Later', 'City': 'San Francisco', 'Create date': '2024-03-23T01:52:36+0000', 'Email': 'georgejurand03@gmail.com', 'First name': 'George', 'How many spots would you like to reserve for our upcoming group trip? (Please specify the number of travelers)': '2', 'Last name': 'Jurand', 'Phone number': '+14155161635', "Select the African destination you're most interested in from our upcoming itineraries": 'GHANA October 15th-24th 2024', 'What will be the best time to reach you?': '2024-03-27T02:00:00+0000'}
# # Normalize and update the structure of the required_contact_details to match the normalized keys
# # required_contact_details = {normalize_key(k) for k in {
# #     'first_name', 'last_name', 'email', 'phone_number', 'gender', 'state'
# # }}

# # Adjust the function call if necessary

# standardized_data = standardized_model_facebook(raw_data)
# print(standardized_data)


