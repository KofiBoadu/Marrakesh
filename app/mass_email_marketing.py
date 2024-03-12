import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed
from  .models import create_databaseConnection
import logging
import boto3
from botocore.exceptions import ClientError


load_dotenv()



aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_default_region = os.getenv('AWS_DEFAULT_REGION')



# def marketing_Email(user_id, total_email_list, campaign_subject, campaign_body, campaign_status="sent"):
#     query = """
#         INSERT INTO marketing_emails
#         (user_id, total_email_list, campaign_subject, campaign_body, campaign_status)
#         VALUES (%s, %s, %s, %s, %s)
#     """
#     database_connection = None
#     cursor = None
#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, (user_id, total_email_list, campaign_subject, campaign_body, campaign_status))
#         database_connection.commit()
#         return cursor.rowcount > 0
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         if database_connection is not None:
#             database_connection.rollback()
#         return False
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if database_connection is not None:
#             database_connection.close()


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
        campaign_id = cursor.lastrowid  # Get the generated campaign_id
        database_connection.commit()
        return campaign_id  # Return the campaign_id
    except Exception as e:
        print(f"An error occurred: {e}")
        if database_connection is not None:
            database_connection.rollback()
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()








# def send_email_marketing(customer_name, receiver_email, subject, sender_email, text_body, configuration_set_name='EmailEventTrackingSet'):
#     # AWS Region (make sure this matches your SES region)
#     aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-2")

#     # Initialize SES client
#     ses_client = boto3.client('ses', region_name=aws_region)

#     # HTML version of your email body
#     html_body = f"""<html>
#                     <body>
#                         <p>Dear {customer_name},</p>
#                         <p>{text_body}</p>
#                     </body>
#                 </html>"""

#     try:
#         # Send email
#         response = ses_client.send_email(
#             Source=sender_email,
#             Destination={'ToAddresses': [receiver_email]},
#             Message={
#                 'Subject': {'Data': subject},
#                 'Body': {
#                     'Html': {'Data': html_body},
#                     'Text': {'Data': text_body},
#                 }
#             },
#             ConfigurationSetName=configuration_set_name
#         )
#         print(f"Email sent successfully to {receiver_email}. Message ID: {response['MessageId']}")
#     except ClientError as e:
#         print(f"Failed to send email to {receiver_email}: {e.response['Error']['Message']}")


def send_email_marketing(customer_name, receiver_email, subject, sender_email, text_body, campaign_id, configuration_set_name='EmailEventTrackingSet'):
    aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-2")
    ses_client = boto3.client('ses', region_name=aws_region)
    html_body = f"""<html><body><p>Dear {customer_name},</p><p>{text_body}</p></body></html>"""

    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [receiver_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': html_body}, 'Text': {'Data': text_body}},
            },
            Tags=[{'Name': 'campaign_id', 'Value': str(campaign_id)}],  # Include campaign_id as a tag
            ConfigurationSetName=configuration_set_name
        )
        print(f"Email sent successfully to {receiver_email}. Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Failed to send email to {receiver_email}: {e.response['Error']['Message']}")







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








# def send_email_marketing(customer_name, receiver_email, subject, sender_email, text_body, smtp_settings=smtp_settings, configuration_set_name='EmailEventTrackingSet'):
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     # Add configuration set header with the default or provided configuration set name
#     msg.add_header('X-SES-CONFIGURATION-SET', configuration_set_name)

#     # Plain text version
#     part1 = MIMEText(text_body, 'plain')
#     # HTML version
#     html_body = f"""<html>
#                     <body>
#                         <p>Dear {customer_name},</p>
#                         <p>{text_body}</p>
#                     </body>
#                 </html>"""
#     part2 = MIMEText(html_body, 'html')

#     msg.attach(part1)
#     msg.attach(part2)

#     try:
#         with smtplib.SMTP(smtp_settings['server'], smtp_settings['port']) as server:
#             server.ehlo()
#             if smtp_settings['tls']:
#                 server.starttls()
#                 server.ehlo()
#             server.login(smtp_settings['username'], smtp_settings['password'])
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#             print(f"Email sent successfully to {receiver_email}")
#     except Exception as e:
#         print(f"Failed to send email to {receiver_email}: {e}")











def send_emails_asynchronously(recipients_list, subject, sender_email, text_body,campaign_id):
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_email_marketing, name, email, subject, sender_email, text_body,campaign_id) for name, email in recipients_list]
        for future in as_completed(futures):
            try:
                future.result()  # Wait for each email to be sent and handle exceptions here
            except Exception as e:
                print(f"Email sending failed with error: {e}")





