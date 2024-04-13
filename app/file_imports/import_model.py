# from app.models import add_new_contact,check_contact_exists
from app.utils.database  import create_database_connection
import logging
import io
import csv
import re


HEADER_MAPPING = {
    'first_name': ['first name', 'firstname', 'first', 'fname'],
    'last_name': ['last name', 'lastname', 'last', 'lname', 'surname'],
    'email': ['email', 'email_address', 'email address'],
    'phone': ['phone number', 'phonenumber', 'phone', 'mobile', 'contact'],
    'gender': ['gender', 'sex'],
    'state': ['state', 'province', 'region', 'location'],
    'lead_status': ['lead status', 'status']
}


def clean_phone_number(phone_number):
    # Remove any characters that are not digits
    cleaned_number = re.sub(r'\D', '', phone_number)
    return cleaned_number



def normalize_header(header):
    """
    Normalize a CSV header to a standardized field name.
    Returns None if the header is not recognized.
    """
    for field, possible_headers in HEADER_MAPPING.items():
        if header.lower() in [ph.lower() for ph in possible_headers]:
            return field
    return None








def add_many_contacts(contacts):
    """
    Adds multiple contacts to the database in a single operation.

    Parameters:
    - contacts (list of tuple): A list of tuples, where each tuple contains the contact details.

    Returns:
    - The number of contacts successfully added to the database.
    """
    query = """
        INSERT INTO contacts
        (first_name, last_name, email_address, phone_number, gender, state_address, lead_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.executemany(query, contacts)
        database_connection.commit()
        print(f"{cursor.rowcount} contacts were successfully added.")
        return cursor.rowcount
    except Exception as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
        return 0
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def fetch_existing_emails():
    """
    Fetches all email addresses from the contacts database.

    Returns:
    - A set of all email addresses (as strings) in the database, transformed to lower case for case-insensitive comparison.
    """
    query = "SELECT LOWER(TRIM(email_address)) FROM contacts"
    emails = set()
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        
        emails = {email[0] for email in cursor.fetchall()}
    except Exception as e:
        logging.error(f"Error occurred while fetching emails: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()

    return emails







def process_csv(file, chunk_size=500):
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)
    
    # Reverse the construction of header_map to map internal names to CSV headers.
    header_map = {}
    for header in csv_input.fieldnames:
        normalized_header = header.lower().strip()
        for internal_name, possible_headers in HEADER_MAPPING.items():
            if normalized_header in [ph.lower().strip() for ph in possible_headers]:
                header_map[internal_name] = header  # Map internal name to the original CSV header
                break

    print("Corrected Header Map:", header_map)
    
    existing_emails = fetch_existing_emails()
    contacts_to_add = []
    processed_count = 0

    for row in csv_input:
  
        email = row.get(header_map.get('email', ''), '').strip().lower()
        print("email from csv:", email)
        if email and email not in existing_emails:
            phone=clean_phone_number(row.get(header_map.get('phone', ''), '').strip())
            contact = (
                row.get(header_map.get('first_name', ''), '').strip(),
                row.get(header_map.get('last_name', ''), '').strip(),
                email,
                phone,
                row.get(header_map.get('gender', ''), '').strip(),
                row.get(header_map.get('state', ''), '').strip(),
                'Lead'  # Default lead status
            )
            print("Adding Contact:", contact)
            contacts_to_add.append(contact)
            if len(contacts_to_add) == chunk_size:
                add_many_contacts(contacts_to_add)
                processed_count += len(contacts_to_add)
                contacts_to_add = []

    if contacts_to_add:
        add_many_contacts(contacts_to_add)
        processed_count += len(contacts_to_add)

    print(f"Total processed contacts: {processed_count}")




