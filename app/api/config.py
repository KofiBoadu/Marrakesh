from flask_httpauth import HTTPBasicAuth
from app.user import get_user
from werkzeug.security import generate_password_hash,check_password_hash
from  app.models import create_database_connection


auth = HTTPBasicAuth()



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



# raw_data = {
#     'First Name': 'Daniel',
#     'Last Name': 'Boadu',
#     'Email ': 'phyllis.kodua@gmail.com',
#     'Phone Number': '2162694794',
#     'How many travelers': '2',
#     'Enter full names and emails  of other travelers if any': '',
#     'What type of tour?': '2024 South Africa October 15th-24th',
#     'Referral Name or Code if any ': '',
#     'How did you hear about us?': '',
#     'City': 'cleveland',
#     'State': 'OH',
#     'Postal / Zip Code': '44113',
#     'Country': 'United States',
#     'Gender': 'Male',
#     'Type of accommodation': 'Double Occupancy',
#     'Payment options': 'Monthly Payment',
#     'Address': '955 west st clair avenue',
#     'What is the best way to contact you?': 'Phone',
#     'If phone, when is the best time of day for a call-back?': '8-11 AM',
#     'Is there anything else we should know?': '',
#     'Deposit amount': '',
#     'Date': 'March 21, 2024',
#     'Time': '11:14 pm',
#     'Page URL': 'https://africatravellers.com/booking-form/?preview_id=5875&preview_nonce=b8026c84e2&preview=true',
#     'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#     'Remote IP': '98.30.182.122',
#     'Powered by': 'Elementor',
#     'form_id': '206b668',
#     'form_name': 'Enquiry form'
# }


# raw_data= {'First Name': 'Daniel', 'Last Name': 'Boadu', 'Email ': 'phyllis.kodua@gmail.com', 'Phone Number': '2162694794', 'Message': "Certainly, to prepare the provided data for testing with your model without changing the naming conventions of the keys, you can use the data directly as it is presented. Here's how you can define it in a Python variable as raw data", 'Date': 'March 21, 2024', 'Time': '11:50 pm', 'Page URL': 'https://africatravellers.com/contact/', 'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Remote IP': '98.30.182.122', 'Powered by': 'Elementor', 'form_id': '34fa04c', 'form_name': 'New Form'}


# standardized_data = create_standardized_model(raw_data)

# print("Standardized Data:", standardized_data)
