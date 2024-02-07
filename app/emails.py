from  .models import create_databaseConnection
from flask_mail import Message
from flask_mail import Mail
from flask import current_app
from datetime import datetime
from flask import  copy_current_request_context
import threading
from email.message import EmailMessage
from concurrent.futures import ThreadPoolExecutor,as_completed



mail = Mail()



def send_email(subject, sender, recipients, text_body):
    with current_app.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        try:
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send email: {e}')
            return False




def send_email_with_context(customer_name, receiver_email, subject, sender, text_body):
    from app import create_app #I initialized and imported the module here to avoid circular import
    app=create_app()
    with app.app_context():
        recipients = [receiver_email]
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = f"""Dear {customer_name},

{text_body}

"""
        msg.html = f"""<html>
<body>
    <p>Dear {customer_name},</p>
    <br>
    <p>{text_body}</p>
</body>
</html>
"""
        try:
            mail.send(msg)
            print("Email sent successfully to", receiver_email)
        except Exception as e:
            current_app.logger.error(f'Failed to send email to {receiver_email}: {e}')








def send_emails_asynchronously(recipients_list, subject, sender, text_body):
    from app import create_app #I initialized and imported the module here to avoid circular import 
    app=create_app()
    with app.app_context():

        with ThreadPoolExecutor(max_workers=10) as executor:

            futures = [executor.submit(send_email_with_context, name, email, subject, sender, text_body) for name, email in recipients_list]

            for future in as_completed(futures):
                try:
                    future.result()  # Wait for each email to be sent and handle exceptions here
                except Exception as e:
                    print(f"Email sending failed with error: {e}")









def customer_email_interactions(customer_id,subject,body,status):
    database_connection= None
    cursor= None
    query="INSERT INTO emails (customer_id, subject, body, status) VALUES (%s, %s, %s, %s)"
    values = (customer_id, subject, body, status)
    try:
        database_connection= create_databaseConnection()
        cursor= database_connection.cursor()
        cursor.execute(query,values)
        database_connection.commit()

    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()







def all_emails_sent_to_customer(customer_id):
    database_connection = None
    cursor = None
    query = "SELECT email_id, subject, status, sent_date, body FROM emails WHERE customer_id = %s ORDER BY email_id DESC"

    all_emails = []
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (customer_id,))
        results = cursor.fetchall()
        all_emails = [{'email_id':email[0],'subject': email[1], 'status': email[2], 'sent_date': email[3], 'body': email[4]} for email in results]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()
    return all_emails








def create_customers_by_year_procedure():
    procedure_query = """
    CREATE PROCEDURE GetCustomersByYearOrAll(IN input_year INT)
    BEGIN
        IF input_year = 1 THEN
            -- Return all customers' first name and email address
            SELECT
                CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                c.email_address AS `Email`
            FROM
                customers c
            ORDER BY
                c.customer_id DESC;
        ELSE
            -- Return customers' first name and email address for the specified year
            SELECT
                CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                c.email_address AS `Email`
            FROM
                customers c
            JOIN
                tour_bookings tb ON tb.customer_id = c.customer_id
            JOIN
                tours t ON tb.tour_id = t.tour_id
            WHERE
                YEAR(t.start_date) = input_year
            ORDER BY
                c.customer_id DESC;
        END IF;
    END;
    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
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






def get_customers_by_year_or_all(input_year):
    database_connection = None
    cursor = None
    customers = []  # Initialize an empty list to store customer data

    try:
        database_connection = create_databaseConnection()
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






def our_customers_sincebyYear():
    start_year= 2023 
    current_year = datetime.now().year
    year_list= [ year for year in range(start_year, current_year+1)]
    return year_list




def delete_customer_email(email_id):
    database_connection = None
    cursor = None
    query = "DELETE FROM emails WHERE email_id = %s"
    try:
        database_connection = create_databaseConnection()
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
