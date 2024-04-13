import phonenumbers
from .database import create_database_connection
from flask_mail import Message, Mail
from flask import current_app
from datetime import datetime
from flask_caching import Cache
from flask_login import LoginManager

cache = Cache(config={'CACHE_TYPE': 'simple'})

login_manager = LoginManager()








mail = Mail()


def send_email(subject, recipients, text_body, sender="bookings@africatravellers.com", html_body=None):
    """
        Sends an email to a list of recipients with a specified subject and body.

        Parameters:
        - subject (str): The subject line of the email.
        - recipients (list): A list of email addresses to which the email will be sent.
        - text_body (str): The plain text body of the email.
        - sender (str, optional): The email address from which the email will be sent. Defaults to 'bookings@africatravellers.com'.
        - html_body (str, optional): The HTML body of the email. If provided, the email will be sent as a multipart message with both text and HTML parts.

        Returns:
        - bool: True if the email was sent successfully, False otherwise.

        Note:
        - Uses Flask-Mail's current app context for sending emails. On failure, logs the error using Flask's current app logger.
    """
    with current_app.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        if html_body is not None:
            msg.html = html_body
        try:
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send email: {e}')
            return False



def our_customers_since_by_year():
    """
        Generates a list of years from a predefined start year to the current year.

        Returns:
        - list: A list of years from the start year (2023) to the current year, inclusive.

        Note:
        - Useful for generating year options dynamically for UI elements or reports.
    """
    start_year = 2023
    current_year = datetime.now().year
    year_list = [year for year in range(start_year, current_year + 1)]
    return year_list




def get_customers_by_year_or_all(input_year):
    """
        Retrieves customers' names and email addresses filtered by a specific year or all customers if no year is specified, using a stored procedure.

        Parameters:
        - input_year (int): The year to filter customers by. If input_year is 1, retrieves all customers.

        Returns:
        - list: A list of tuples, each containing a customer's full name and email address, fetched using the stored procedure.

        Raises:
        - Exception: If an error occurs while fetching data, an exception is raised with details of the error.

        Note:
        - Calls a previously defined stored procedure 'GetCustomersByYearOrAll' from the database. Closes the database connection before exiting.
    """
    database_connection = None
    cursor = None
    customers = []
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.callproc('GetCustomersByYearOrAll', [input_year])

        # Iterate over stored results and fetch all data
        for result in cursor.stored_results():
            customers.extend(result.fetchall())
    except Exception as e:
        raise Exception(f"An error occurred while fetching data: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()
    return customers

    



def contact_email_interactions(contact_id, subject, body, status, sent_user):
    """
        Logs an email interaction for a contact in the database.

        Parameters:
        - contact_id (int): The ID of the contact for whom the email interaction is logged.
        - subject (str): The subject of the email interaction.
        - body (str): The body of the email interaction.
        - status (str): The status of the email interaction (e.g., 'sent', 'failed').
        - sent_user (str): Identifier of the user who sent the email.

        Raises:
        - Exception: If an error occurs during the database operation, an exception is raised with details of the error.

        Note:
        - Commits the email interaction to the database and ensures that the database connection is closed before exiting.
    """
    database_connection = None
    cursor = None
    query = "INSERT INTO emails (contact_id, subject, body, status, sent_user) VALUES (%s, %s, %s, %s, %s)"
    values = (contact_id, subject, body, status, sent_user)
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, values)
        database_connection.commit()
    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()




def delete_contacts_email(email_id):
    """
        Deletes an email record from the database based on the provided email ID.

        Parameters:
        - email_id (int): The ID of the email to be deleted.

        Note:
        - Attempts to delete the specified email and commits the transaction. If an error occurs, prints the error message and rolls back the transaction to maintain database integrity. Ensures the database connection is closed before exiting.
    """
    database_connection = None
    cursor = None
    query = "DELETE FROM emails WHERE email_id = %s"
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (email_id,))
        database_connection.commit()
    except Exception as e:
        print(f"An error occurred while deleting the email: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def update_full_contact_details(contact_id, first_name, last_name, email, phone, gender, state):
    """
        Updates the full contact details for a specific contact ID in the database.

        Parameters:
        - contact_id (int): Unique identifier for the contact.
        - first_name (str): The contact's first name.
        - last_name (str): The contact's last name.
        - email (str): The contact's email address.
        - phone (str): The contact's phone number.
        - gender (str): The contact's gender.
        - state (str): The state address of the contact.

        No explicit return value. Prints a message indicating whether the update was successful or if no customer was found.
        """

    query = """
       UPDATE contacts
        SET first_name = %s,
            last_name = %s,
            state_address = %s,
            email_address = %s,
            phone_number = %s,
            gender = %s
        WHERE contact_id = %s
    """
    values = (first_name, last_name, state, email, phone, gender, contact_id)
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            if cursor.rowcount > 0:
                print("Customer details successfully updated for ID:", contact_id)
            else:
                print("No customer found with ID:", contact_id)
    except Exception as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()







def format_phone_number(number, country_code='US'):
    """
        Formats a phone number to the international format based on the specified country code.

        Parameters:
        - number (str): The phone number to format.
        - country_code (str, optional): The ISO country code to which the number belongs. Defaults to 'US'.

        Returns:
        - A string representing the formatted phone number or an empty string if formatting fails.
    """
    if not number:
        return ""
    try:
        user_number = phonenumbers.parse(number, country_code)
        formatted_number = phonenumbers.format_number(user_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return formatted_number
    except phonenumbers.NumberParseException:
        return ""




def all_states():
    """
        Provides a list of US state abbreviations.

        Returns:
        - A list of strings, each being a US state abbreviation.
    """
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return states


