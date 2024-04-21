import json
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from  app.utils.main import create_database_connection
import boto3
from botocore.exceptions import ClientError

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_default_region = os.getenv('AWS_DEFAULT_REGION')


def marketing_email(user_id, total_number_of_email_list, campaign_subject, campaign_body, campaign_status="sent"):
    """
        Creates a new email marketing campaign in the database.

        Parameters:
        - user_id (int): The ID of the user creating the campaign.
        - total_number_of_email_list (int): The total number of emails in the mailing list for this campaign.
        - campaign_subject (str): The subject line of the marketing email.
        - campaign_body (str): The body content of the marketing email.
        - campaign_status (str, optional): The initial status of the campaign (default is 'sent').

        Returns:
        - The ID of the newly created campaign if successful, None otherwise.

        Raises:
        - Prints an error message if the campaign creation fails.
    """
    query = """
        INSERT INTO marketing_emails
        (user_id, total_email_list, campaign_subject, campaign_body, campaign_status)
        VALUES (%s, %s, %s, %s, %s)
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (user_id, total_number_of_email_list, campaign_subject, campaign_body, campaign_status))
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


def enqueue_email_task(recipient_list, subject, sender_email, text_body, campaign_id):
    sqs = boto3.client('sqs', region_name=os.getenv("AWS_DEFAULT_REGION"))
    queue_url = os.getenv("AWS_SQS_URL")
    for name, email in recipient_list:
        message_body = {
            'contact_name': name,
            'receiver_email': email,
            'subject': subject,
            'sender_email': sender_email,
            'text_body': text_body,
            'campaign_id': campaign_id
        }

        try:
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body)
            )

        except Exception as e:

            print(f"Failed to send message for {email} with error: {e}")

    return True





def send_email_marketing(contact_name, receiver_email, subject, sender_email, text_body, campaign_id,
                         configuration_set_name='EmailEventTrackingSet'):
    """
        Sends an individual marketing email using AWS SES.

        Parameters:
        - contact_name (str): The name of the email recipient.
        - receiver_email (str): The email address of the recipient.
        - subject (str): The subject line of the email.
        - sender_email (str): The email address of the sender.
        - text_body (str): The text body of the email.
        - campaign_id (int): The campaign ID associated with this email.
        - configuration_set_name (str, optional): The SES configuration set name for email event tracking.

        Note:
        - Prints the success or failure message of the email sending operation.
    """

    aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-2")
    ses_client = boto3.client('ses', region_name=aws_region)
    html_body = f" Dear {contact_name},{text_body}"

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
    """
        Retrieves all email campaigns from the database with their delivery statistics.

        Returns:
        - A list of tuples containing campaign details and metrics or an empty list if an error occurs.

        Note:
        - Each tuple includes the campaign subject, total email list count, sent date, campaign ID, creator's full name, and metrics like delivery and open rates.
        - Prints an error message in case of a failure.
    """
    query = """
       SELECT
        m.campaign_subject,
        m.total_email_list,
        m.sent_date,
        m.campaign_id,
        CONCAT(u.first_name, ' ', u.last_name) AS full_name,
        COUNT(DISTINCT CASE WHEN em.event_type = 'Delivery' THEN em.contact_id END) AS delivered,
        ROUND(COUNT(DISTINCT CASE WHEN em.event_type = 'Open' THEN em.contact_id END) * 100.0 / NULLIF(COUNT(DISTINCT CASE WHEN em.event_type = 'Delivery' THEN em.contact_id END), 0), 2) AS unique_open_rate,
        ROUND(COUNT(DISTINCT CASE WHEN em.event_type = 'Click' THEN em.contact_id END) * 100.0 / NULLIF(COUNT(DISTINCT CASE WHEN em.event_type = 'Delivery' THEN em.contact_id END), 0), 2) AS unique_click_rate
        FROM marketing_emails AS m
        JOIN users AS u ON m.user_id = u.user_id
        LEFT JOIN marketing_email_metrics AS em ON m.campaign_id = em.campaign_id
        GROUP BY m.campaign_id, m.campaign_subject, m.total_email_list, m.sent_date, full_name
        ORDER BY m.sent_date DESC

    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
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



def get_email_campaign_subject(campaign_id):
    query = "SELECT campaign_subject FROM marketing_emails WHERE campaign_id = %s"
    database_connection = None 
    cursor = None 
    try:
        database_connection= create_database_connection()
        cursor= database_connection.cursor()
        cursor.execute(query, (campaign_id,))
        subject= cursor.fetchone()
        if subject:
            return subject[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None 

    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()








def campaign_open_rate(campaign_id):
    """
        Calculates the open rate of a specific email campaign.

        Parameters:
        - campaign_id (int): The ID of the campaign for which to calculate the open rate.

        Returns:
        - The open rate of the campaign as a percentage or None if an error occurs.

        Note:
        - Calculates the open rate based on the adjusted number of deliveries (excluding bounces) and unique opens.
        - Prints an error message in case of a failure.
    """
    query = """
    SELECT
        COUNT(DISTINCT CASE WHEN event_type = 'Open' THEN contact_id END) as unique_opens,
        COUNT(DISTINCT CASE WHEN event_type = 'Delivery' THEN contact_id END) as deliveries,
        COUNT(DISTINCT CASE WHEN event_type = 'Bounce' THEN contact_id END) as bounces
    FROM marketing_email_metrics
    WHERE campaign_id = %s
    GROUP BY campaign_id
    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (campaign_id,))
        results = cursor.fetchone()

        unique_opens, deliveries, bounces = results

        adjusted_deliveries = deliveries - bounces

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
    """
        Executes a given SQL query with a campaign_id parameter and returns the first result.

        Parameters:
        - query (str): The SQL query to execute.
        - campaign_id (int): The campaign ID to use in the query.

        Returns:
        - The first column of the first row of the query result or 0 if no result is found or an error occurs.

        Note:
        - Designed for usability in fetching various campaign metrics.
        - Prints an error message in case of a failure.
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
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
    """
        Retrieves the number of unique opens for a specific email campaign.

        Parameters:
        - campaign_id (int): The ID of the campaign.

        Returns:
        - The number of unique opens.
    """
    query = """
    SELECT COUNT(DISTINCT contact_id)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Open'
    """

    return execute_query(query, campaign_id)


def get_total_opens(campaign_id):
    query = """
    SELECT COUNT(*)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Open'
    """

    return execute_query(query, campaign_id)


def get_click_rate(campaign_id):
    """
        Calculates the click rate of a specific email campaign.

        Parameters:
        - campaign_id (int): The ID of the campaign.

        Returns:
        - The click rate of the campaign as a percentage.
    """
    unique_clicks = get_unique_clicks(campaign_id)
    deliveries = get_deliveries(campaign_id) - get_bounces(campaign_id)
    click_rate = (unique_clicks / deliveries) * 100 if deliveries > 0 else 0
    return click_rate


def get_unique_clicks(campaign_id):
    # SQL query to get the number of unique clicks
    query = """
    SELECT COUNT(DISTINCT contact_id)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Click'
    """

    return execute_query(query, campaign_id)


def get_total_clicks(campaign_id):
    query = """
    SELECT COUNT(*)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Click'
    """
    return execute_query(query, campaign_id)


def get_deliveries(campaign_id):
    """
        Retrieves the total number of successful deliveries for a specific email campaign.

        Parameters:
        - campaign_id (int): The ID of the campaign.

        Returns:
        - The total number of deliveries.
    """
    query = """
    SELECT COUNT(*)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Delivery'
    """
    return execute_query(query, campaign_id)


def get_bounces(campaign_id):
    query = """
    SELECT COUNT(DISTINCT contact_id)
    FROM marketing_email_metrics
    WHERE campaign_id = %s AND event_type = 'Bounce'
    """
    return execute_query(query, campaign_id)


def get_successful_deliveries(campaign_id):
    query = ("SELECT COUNT(DISTINCT contact_id) FROM marketing_email_metrics WHERE event_type = 'Delivery' AND "
             "campaign_id = %s")
    return execute_query(query, campaign_id)


def get_unsubscribes(campaign_id):
    query = ("SELECT COUNT(DISTINCT contact_id) FROM marketing_email_metrics WHERE event_type = 'Subscription' AND "
             "campaign_id = %s")
    return execute_query(query, campaign_id)


def get_spam_reports(campaign_id):
    query = ("SELECT COUNT(DISTINCT contact_id) FROM marketing_email_metrics WHERE event_type = 'Complaint' AND "
             "campaign_id = %s")
    return execute_query(query, campaign_id)


def get_total_sent(campaign_id):
    query = "SELECT COUNT(DISTINCT contact_id) FROM marketing_email_metrics WHERE campaign_id = %s"
    return execute_query(query, campaign_id)


def get_percentage(count, total):
    return round((count / total) * 100) if total > 0 else 0


def get_event_metrics(campaign_id):
    """
        Aggregates and returns key email event metrics for a specific campaign.

        Parameters:
        - campaign_id (int): The ID of the campaign.

        Returns:
        - A dictionary with keys for successful deliveries, delivery percentage, bounces, bounce percentage, unsubscribes, unsubscribe percentage, spam reports, and spam report percentage.
    """
    total_sent = get_total_sent(campaign_id)
    successful_deliveries = get_successful_deliveries(campaign_id)
    bounces = get_bounces(campaign_id)
    unsubscribes = get_unsubscribes(campaign_id)
    spam_reports = get_spam_reports(campaign_id)

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


# def get_customer_campaign_events(campaign_id):
#     query = """
#         SELECT
#             c.contact_id,
#             CONCAT(c.first_name, ' ', c.last_name) AS full_name,
#             m.campaign_id,
#             m.event_type
#         FROM contacts c
#         JOIN (
#             SELECT
#                 contact_id,
#                 campaign_id,
#                 event_type,
#                 MAX(metric_id) AS MaxMetricId
#             FROM marketing_email_metrics
#             WHERE campaign_id = %s
#             GROUP BY contact_id
#         ) AS LatestEvent ON c.contact_id = LatestEvent.contact_id
#         JOIN marketing_email_metrics m ON m.contact_id = LatestEvent.contact_id AND m.metric_id = LatestEvent.MaxMetricId
#     """
#     database_connection = None
#     cursor = None
#     try:
#         database_connection = create_database_connection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, (campaign_id,))
#         results = cursor.fetchall()
#         return results
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()




def campaign_events_procedure():
    create_procedure_query = """
        CREATE PROCEDURE GetCampaignEvents(
            IN _campaign_id INT,
            IN _items_per_page INT,
            IN _page_number INT
        )
        BEGIN
            DECLARE _offset INT DEFAULT (_page_number - 1) * _items_per_page;
            
            SELECT
                c.contact_id,
                CONCAT(c.first_name, ' ', c.last_name) AS full_name,
                m.campaign_id,
                m.event_type
            FROM contacts c
            JOIN (
                SELECT
                    contact_id,
                    campaign_id,
                    event_type,
                    MAX(metric_id) AS MaxMetricId
                FROM marketing_email_metrics
                WHERE campaign_id = _campaign_id
                GROUP BY contact_id
            ) AS LatestEvent ON c.contact_id = LatestEvent.contact_id
            JOIN marketing_email_metrics m ON m.contact_id = LatestEvent.contact_id AND m.metric_id = LatestEvent.MaxMetricId
            ORDER BY c.contact_id
            LIMIT _items_per_page OFFSET _offset;
        END;
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS GetCampaignEvents")
        cursor.execute(create_procedure_query)
        database_connection.commit()
        print("Stored procedure created successfully.")
        return True
    except Exception as e:
        raise Exception(f"An error occurred while creating the procedure: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

  



def get_customer_campaign_events(campaign_id, page, per_page=10):
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.callproc('GetCampaignEvents', [campaign_id, per_page, page])
        results = []
        for result in cursor.stored_results():  
            results.extend(result.fetchall())
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()



# print(get_customer_campaign_events(21,2,25))













def delete_campaign(campaign_id):
    """
        Deletes a specific email campaign from the database.

        Parameters:
        - campaign_id (int): The ID of the campaign to delete.

        Returns:
        - True if the campaign was successfully deleted, False otherwise.

        Note:
        - Rolls back the transaction in case of an error and prints an error message.
    """
    query = """DELETE FROM marketing_emails WHERE campaign_id = %s"""
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (campaign_id,))
        database_connection.commit()
        return True
    except Exception as e:
        if database_connection is not None:
            database_connection.rollback()
        print(f"An error occurred: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


def send_emails_asynchronously(recipients_list, subject, sender_email, text_body, campaign_id):
    """
        Sends marketing emails asynchronously to a list of recipients using AWS SES.

        This function dispatches emails in parallel to improve performance and response time, especially useful when sending large volumes of emails. Each email is personalized and sent individually to each recipient in the list.

        Parameters:
        - recipients_list (list of tuples): A list where each tuple contains the recipient's name and email address, structured as (name, email).
        - subject (str): The subject line of the email to be sent.
        - sender_email (str): The email address from which the email will be sent.
        - text_body (str): The plain text body of the email.
        - campaign_id (int): The ID of the marketing campaign associated with these emails.

        Note:
        - Utilizes a ThreadPoolExecutor to manage parallel tasks, sending emails concurrently across multiple threads.
        - Handles and logs any exceptions that occur during the email sending process to ensure the application remains robust.
        - This function assumes the `send_email_marketing` function is defined and correctly implements sending emails via AWS SES, including handling necessary AWS credentials and setup.
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_email_marketing, name, email, subject, sender_email, text_body, campaign_id) for
                   name, email in recipients_list]
        for future in as_completed(futures):
            try:
                future.result()  # Wait for each email to be sent and handle exceptions here
            except Exception as e:
                print(f"Email sending failed with error: {e}")
