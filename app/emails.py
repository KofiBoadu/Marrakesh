from  .models import create_databaseConnection
from flask_mail import Message
from flask_mail import Mail
from flask import current_app
from datetime import datetime
import asyncio
import aiosmtplib
from email.message import EmailMessage
from flask import current_app





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





async def send_marketing_email(recipient, subject, text_body, name, smtp_settings):
    msg = EmailMessage()
    msg["From"] = smtp_settings["MAIL_USERNAME"]
    msg["To"] = recipient
    msg["Subject"] = subject

    # Plain text body
    msg.set_content(f"""Dear {name},

{text_body}
""")

    # HTML body
    msg.add_alternative(f"""<html>
        <body>
            <p>Dear {name},</p>
            <br>
            <p>{text_body}</p>
        </body>
    </html>
    """, subtype='html')

    await aiosmtplib.send(
        msg,
        hostname=smtp_settings["MAIL_SERVER"],
        port=smtp_settings["MAIL_PORT"],
        username=smtp_settings["MAIL_USERNAME"],
        password=smtp_settings["MAIL_PASSWORD"],
        use_tls=smtp_settings["MAIL_USE_SSL"]
    )



async def mass_send_emailTemplate(subject, sender, recipients, text_body, batch_size=10, wait_time=60):
    smtp_settings = {
        "MAIL_SERVER": current_app.config["MAIL_SERVER"],
        "MAIL_PORT": current_app.config["MAIL_PORT"],
        "MAIL_USERNAME": current_app.config["MAIL_USERNAME"],
        "MAIL_PASSWORD": current_app.config["MAIL_PASSWORD"],
        "MAIL_USE_SSL": current_app.config["MAIL_USE_SSL"]
    }

    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i+batch_size]
        tasks = [asyncio.create_task(send_marketing_email(recipient_email, subject, text_body, recipient_name, smtp_settings))
                 for recipient_name, recipient_email in batch]

        await asyncio.gather(*tasks)
        await asyncio.sleep(wait_time)  # Wait for a specified time before sending the next batch

    return True  # Returns True when all emails are sent












# async def mass_send_emailTemplate(subject, sender, recipients, text_body):
#     smtp_settings = {
#         "MAIL_SERVER": current_app.config["MAIL_SERVER"],
#         "MAIL_PORT": current_app.config["MAIL_PORT"],
#         "MAIL_USERNAME": current_app.config["MAIL_USERNAME"],
#         "MAIL_PASSWORD": current_app.config["MAIL_PASSWORD"],
#         "MAIL_USE_SSL": current_app.config["MAIL_USE_SSL"]
#     }

#     tasks = []
#     for receipient_name,receipient_email in recipients:
#         task = asyncio.create_task(send_marketing_email(receipient_email, subject, text_body, receipient_name, smtp_settings))
#         tasks.append(task)

#     results = await asyncio.gather(*tasks)
#     return all(results)












# def mass_send_emailTemplate(subject, sender, recipients, text_body, name):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = f"""Dear {name},

#             {text_body}

#              """
#     msg.html = f"""<html>
#         <body>
#             <p>Dear {name},</p>
#              <br>
#              <p>{text_body}</p>
#         </body>
#     </html>
#     """
#     try:
#         current_app.mail.send(msg)
#         return True
#     except Exception as e:
#         current_app.logger.error(f'Failed to send email: {e}')
#         return False



# def send_async_email(subject, sender, recipients, text_body, name):
#     with current_app.app_context():
#         return mass_send_emailTemplate(subject, sender, recipients, text_body, name)



# @rq.job
# def send_email_job(subject, sender, recipients, text_body, name):
#     return send_async_email(subject, sender, recipients, text_body, name)


# @rq.job
# def queue_emails_batch(email_data):
#     from_address = email_data['from_address']
#     email_subject = email_data['email_subject']
#     email_body = email_data['email_body']
#     email_list = email_data['email_list']

#     for name, email in email_list:
#         send_email_job.queue(email_subject, from_address, [email], email_body, name)




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
