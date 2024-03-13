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
        m.campaign_id,
        CONCAT(u.first_name, ' ', u.last_name) AS full_name,
        COUNT(DISTINCT CASE WHEN em.event_type = 'Delivery' THEN em.customer_id END) AS delivered,
        ROUND(COUNT(DISTINCT CASE WHEN em.event_type = 'Open' THEN em.customer_id END) * 100.0 / NULLIF(COUNT(DISTINCT CASE WHEN em.event_type = 'Delivery' THEN em.customer_id END), 0), 2) AS unique_open_rate,
        ROUND(COUNT(DISTINCT CASE WHEN em.event_type = 'Click' THEN em.customer_id END) * 100.0 / NULLIF(COUNT(DISTINCT CASE WHEN em.event_type = 'Delivery' THEN em.customer_id END), 0), 2) AS unique_click_rate
        FROM marketing_emails AS m
        JOIN users AS u ON m.user_id = u.user_id
        LEFT JOIN marketing_email_metrics AS em ON m.campaign_id = em.campaign_id
        GROUP BY m.campaign_id, m.campaign_subject, m.total_email_list, m.sent_date, full_name

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
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection and database_connection.is_connected():
            database_connection.close()







def campaign_open_rate(campaign_id):

    query = """
    SELECT
        COUNT(DISTINCT CASE WHEN event_type = 'Open' THEN customer_id END) as unique_opens,
        COUNT(DISTINCT CASE WHEN event_type = 'Delivery' THEN customer_id END) as deliveries,
        COUNT(DISTINCT CASE WHEN event_type = 'Bounce' THEN customer_id END) as bounces
    FROM marketing_email_metrics
    WHERE campaign_id = %s
    GROUP BY campaign_id
    """


    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (campaign_id,))
        results = cursor.fetchone()

        unique_opens, deliveries, bounces = results

        # Calculate the adjusted deliveries by subtracting bounces from deliveries
        adjusted_deliveries = deliveries - bounces

        # Calculate the open rate using the adjusted deliveries
        open_rate = (unique_opens / adjusted_deliveries) * 100 if adjusted_deliveries > 0 else 0

        return open_rate

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()







def execute_query(query, campaign_id):
    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (campaign_id,))
        result = cursor.fetchone()
        return result[0] if result else 0

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()







def get_unique_opens(campaign_id):
    # SQL query to get the number of unique opens
    query = """
    SELECT COUNT(DISTINCT customer_id)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Open'
    """

    return execute_query(query, campaign_id)






def get_total_opens(campaign_id):
    # SQL query to get the total number of opens (including multiple opens by the same user)
    query = """
    SELECT COUNT(*)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Open'
    """

    return execute_query(query, campaign_id)







def get_click_rate(campaign_id):
    unique_clicks = get_unique_clicks(campaign_id)  # This should be the number of unique clicks
    deliveries = get_deliveries(campaign_id) - get_bounces(campaign_id)  # Subtract bounces to get actual deliveries

    # Calculate the click rate using the unique clicks and actual deliveries
    click_rate = (unique_clicks / deliveries) * 100 if deliveries > 0 else 0
    return click_rate





def get_unique_clicks(campaign_id):
    # SQL query to get the number of unique clicks
    query = """
    SELECT COUNT(DISTINCT customer_id)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Click'
    """

    return execute_query(query, campaign_id)




def get_total_clicks(campaign_id):
    # SQL query to get the total number of clicks (including multiple clicks by the same user)
    query = """
    SELECT COUNT(*)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Click'
    """

    return execute_query(query, campaign_id)



def get_deliveries(campaign_id):

    query = """
    SELECT COUNT(*)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Delivery'
    """

    return execute_query(query, campaign_id)



def get_bounces(campaign_id):
    query = """
    SELECT COUNT(DISTINCT customer_id)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Bounce'
    """

    return execute_query(query, campaign_id)

def get_successful_deliveries(campaign_id):
    query = "SELECT COUNT(DISTINCT customer_id) FROM marketing_email_metrics WHERE event_type = 'Delivery' AND campaign_id = %s"
    return execute_query(query, campaign_id)



def get_unsubscribes(campaign_id):
    query = "SELECT COUNT(DISTINCT customer_id) FROM marketing_email_metrics WHERE event_type = 'Subscription' AND campaign_id = %s"
    return execute_query(query, campaign_id)

def get_spam_reports(campaign_id):
    query = "SELECT COUNT(DISTINCT customer_id) FROM marketing_email_metrics WHERE event_type = 'Complaint' AND campaign_id = %s"
    return execute_query(query, campaign_id)




def get_total_sent(campaign_id):
    query = "SELECT COUNT(DISTINCT customer_id) FROM marketing_email_metrics WHERE campaign_id = %s"
    return execute_query(query, campaign_id)






def get_percentage(count, total):
    return round((count / total) * 100) if total > 0 else 0



def get_event_metrics(campaign_id):
    total_sent = get_total_sent(campaign_id)  # Function to get the total number of emails sent for the campaign
    successful_deliveries = get_successful_deliveries(campaign_id)
    bounces = get_bounces(campaign_id)
    unsubscribes = get_unsubscribes(campaign_id)
    spam_reports = get_spam_reports(campaign_id)


    # Calculate percentages
    delivery_percentage = get_percentage(successful_deliveries, total_sent)
    bounce_percentage = get_percentage(bounces, total_sent)
    unsubscribe_percentage = get_percentage(unsubscribes, total_sent)
    spam_report_percentage = get_percentage(spam_reports, total_sent)

    return {


        'successful_deliveries': successful_deliveries,
        'delivery_percentage': delivery_percentage,
        'bounces': bounces,
        'bounce_percentage': bounce_percentage,
        'unsubscribes': unsubscribes,
        'unsubscribe_percentage': unsubscribe_percentage,
        'spam_reports': spam_reports,
        'spam_report_percentage': spam_report_percentage
    }



def total_email_list(campaign_id):
    query = "SELECT total_email_list FROM marketing_emails WHERE campaign_id = %s"
    return execute_query(query, campaign_id)





def send_emails_asynchronously(recipients_list, subject, sender_email, text_body,campaign_id):
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_email_marketing, name, email, subject, sender_email, text_body,campaign_id) for name, email in recipients_list]
        for future in as_completed(futures):
            try:
                future.result()  # Wait for each email to be sent and handle exceptions here
            except Exception as e:
                print(f"Email sending failed with error: {e}")





