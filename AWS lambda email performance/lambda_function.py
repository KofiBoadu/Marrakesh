import os
import json
import mysql.connector
from urllib.parse import urlparse
import logging




#creates a connection my database
def create_databaseConnection():
    database_url = os.getenv('JAWSDB_URL')
    if database_url:
        parsed_url = urlparse(database_url)
        db_user = parsed_url.username
        db_password = parsed_url.password
        db_host = parsed_url.hostname
        db_name = parsed_url.path.lstrip('/')
        db_port = parsed_url.port
        try:
            sql_connection = mysql.connector.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                database=db_name,
                port=db_port
            )
            return sql_connection
        except mysql.connector.Error as e:
            logging.error(f"An error occurred while connecting to the database: {e}")
    else:
        logging.error("DATABASE_URL not set")
        raise ValueError("DATABASE_URL not set")



#this function gets the customer ID
def get_contact_id(email_address, connection):
    cursor = connection.cursor(dictionary=True)
    try:
        sql = "SELECT contact_id FROM contacts WHERE email_address = %s"
        cursor.execute(sql, (email_address,))
        result = cursor.fetchone()
        return result['contact_id'] if result else None
    finally:
        cursor.close()



#inserts the metrics to my metrics table
def insert_event_data(campaign_id, contact_id, event_type, event_timestamp, connection):
    cursor = connection.cursor()
    try:
        sql = """
            INSERT INTO marketing_email_metrics (campaign_id, contact_id, event_type, event_timestamp)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (campaign_id, contact_id, event_type, event_timestamp))
        connection.commit()
        print(f"Inserted event data for campaign_id: {campaign_id}, customer_id: {contact_id} event type:  {event_type}")
    finally:
        cursor.close()





def lambda_handler(event, context):
    for record in event['Records']:
        sns_message = json.loads(record['Sns']['Message'])
        print(json.dumps(sns_message, indent=2))  # This will print the formatted JSON of the SNS message.

        # Ensure these values are extracted according to your message format
        campaign_id = int(sns_message['mail']['tags']['campaign_id'][0])
        event_type = sns_message['eventType']
        print(event_type)
        email_address = sns_message['mail']['destination'][0]
        event_timestamp = sns_message['mail']['timestamp']

        connection = create_databaseConnection()
        if connection:
            try:
                contact_id = get_contact_id(email_address, connection)
                if contact_id:
                    insert_event_data(campaign_id, contact_id, event_type, event_timestamp, connection)
                else:
                    print(f"No customer_id found for {email_address}")
            finally:
                connection.close()
        else:
            print("Failed to establish database connection.")
