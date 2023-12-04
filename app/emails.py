# from .models import create_databaseConnection
from  .models import create_databaseConnection
from flask_mail import Message
from flask_mail import Mail

mail = Mail()

def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    try:
        mail.send(msg)
        return True
    except Exception as e:

        return False




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
