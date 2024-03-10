import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed
from  .models import create_databaseConnection
import logging


load_dotenv()



smtp_settings={
        'server': 'email-smtp.us-east-2.amazonaws.com',
        'port': 587,  
        'username': os.getenv('SES_USERNAME'),
        'password': os.getenv('SES_PASSWORD'),
        'tls': True  
    }




def marketing_Email(user_id, total_email_list, campaign_subject, campaign_body, campaign_status="sent"):
    query = """
        INSERT INTO marketing_emails
        (user_id, total_email_list, campaign_subject, campaign_body, campaign_status)
        VALUES (%s, %s, %s, %s, %s)
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (user_id, total_email_list, campaign_subject, campaign_body, campaign_status))
        database_connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"An error occurred: {e}")
        if database_connection is not None:
            database_connection.rollback()
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()






def all_email_campaign():
    query = """
        SELECT
            m.campaign_subject,
            m.total_email_list,
            m.sent_date,
            CONCAT(u.first_name, ' ', u.last_name) AS full_name
        FROM marketing_emails AS m
        JOIN users AS u ON m.user_id = u.user_id
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"An error occurred: {e}")  # Log or print the exception information.
        if database_connection:
            database_connection.close()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection and database_connection.is_connected():
            database_connection.close()









def send_email_marketing(customer_name, receiver_email, subject, sender_email, text_body, smtp_settings=smtp_settings, configuration_set_name='EmailTrackingSet'):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    # Add configuration set header with the default or provided configuration set name
    msg.add_header('X-SES-CONFIGURATION-SET', configuration_set_name)

    # Plain text version
    part1 = MIMEText(text_body, 'plain')
    # HTML version
    html_body = f"""<html>
                    <body>
                        <p>Dear {customer_name},</p>
                        <p>{text_body}</p>
                    </body>
                </html>"""
    part2 = MIMEText(html_body, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP(smtp_settings['server'], smtp_settings['port']) as server:
            server.ehlo()
            if smtp_settings['tls']:
                server.starttls()
                server.ehlo()
            server.login(smtp_settings['username'], smtp_settings['password'])
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {e}")











def send_emails_asynchronously(recipients_list, subject, sender_email, text_body):
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_email_marketing, name, email, subject, sender_email, text_body) for name, email in recipients_list]
        for future in as_completed(futures):
            try:
                future.result()  # Wait for each email to be sent and handle exceptions here
            except Exception as e:
                print(f"Email sending failed with error: {e}")





