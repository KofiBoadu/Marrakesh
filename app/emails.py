from .models import create_database_connection
from flask_mail import Message, Mail
from flask import current_app
from datetime import datetime

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


def all_emails_sent_to_contacts(contact_id):
    """
        Retrieves all emails sent to a specific contact, ordered by the most recent.

        Parameters:
        - contact_id (int): The ID of the contact whose emails are to be retrieved.

        Returns:
        - list: A list of dictionaries, each representing an email sent to the contact. Includes email ID, subject, status, sent date, body, and the user who sent the email.

        Note:
        - Handles database exceptions by printing an error message but returns an empty list in such cases to ensure the function always returns a list.
    """
    database_connection = None
    cursor = None
    query = ("SELECT email_id, subject, status, sent_date, body, sent_user FROM emails WHERE contact_id = %s ORDER BY "
             "email_id DESC")
    all_emails = []
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        all_emails = [
            {'email_id': email[0], 'subject': email[1], 'status': email[2], 'sent_date': email[3], 'body': email[4],
             "sent_user": email[5]} for email in results]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()
    return all_emails


def create_customers_by_year_procedure():
    """
      Creates a stored procedure in the database that fetches customer information by year or all customers if no year is specified.

      The stored procedure, named 'GetCustomersByYearOrAll', accepts an input year. If the input year is 1, it returns all customers; otherwise, it returns customers associated with the specified year based on tour booking dates.

      Raises:
      - Exception: If an error occurs during the creation of the procedure, an exception is raised with details of the error.

      Note:
      - Before creating the new procedure, any existing procedure with the same name is dropped. The database connection is closed before exiting.
    """
    procedure_query = """
    CREATE PROCEDURE GetCustomersByYearOrAll(IN input_year INT)
    BEGIN
        IF input_year = 1 THEN
            -- Return all customers' first name and email address
            SELECT
                CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                c.email_address AS `Email`
            FROM
                contacts c
            ORDER BY
                c.contact_id DESC;
        ELSE
            -- Return customers' first name and email address for the specified year
            SELECT
                CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                c.email_address AS `Email`
            FROM
                contacts c
            JOIN
                tour_bookings tb ON tb.contact_id = c.contact_id
            JOIN
                tours t ON tb.tour_id = t.tour_id
            WHERE
                YEAR(t.start_date) = input_year
            ORDER BY
                c.contact_id DESC;
        END IF;
    END;
    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS GetCustomersByYearOrAll")
        cursor.execute(procedure_query)
        database_connection.commit()
    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


# print("created",create_customers_by_year_procedure())


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
