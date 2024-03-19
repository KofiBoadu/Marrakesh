import pandas as pd
from app.models import create_database_connection, get_customers_information,total_customers
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from flask_mail import Message
from flask import current_app
from flask_mail import Mail
from app.emails import send_email

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.file']


mail= Mail()







def send_file_email(subject, sender, recipients, text_body, html_body=None):
    from app import create_app
    app = create_app()

    with app.app_context():
        mail = current_app.extensions.get('mail')
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








def export_data(contacts, file_format):
    # Convert customers list to DataFrame
    df = pd.DataFrame(contacts, columns=['Full_Name', 'State', 'Email', 'Mobile', 'Tour', 'Travel_Year_Start', 'Tour_Price', 'Tour_Type'])
    
    # Define the base path for temporary storage
    base_path = '/tmp/'
    
    # Choose the file format
    file_name = ""
    if file_format.lower() == 'csv':
        file_name = "CustomerTourDetails.csv"
        df.to_csv(os.path.join(base_path, file_name), index=False)
        
    elif file_format.lower() == 'excel':
        file_name = "CustomerTourDetails.xlsx"
        df.to_excel(os.path.join(base_path, file_name), index=False)
        
    else:
        print('Unsupported export format specified. No export performed.')

    return os.path.join(base_path, file_name)








def create_export_customer_data_procedure():
    procedure_query = """
    CREATE PROCEDURE ExportCustomerData()
    BEGIN
        SELECT
            CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
            c.state_address AS `State`,
            c.email_address AS `Email`,
            c.phone_number AS `Mobile`,
            t.tour_name AS `Tour`,
            YEAR(t.start_date) AS `Travel_Year_Start`,
            t.tour_price AS `Tour_Price`,
            t.tour_type AS `Tour_Type`
        FROM
            contacts c
        JOIN
            tour_bookings tb ON tb.customer_id = c.customer_id
        JOIN
            tours t ON tb.tour_id = t.tour_id;
    END;
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS ExportCustomerData")
        cursor.execute(procedure_query)
        database_connection.commit()
    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()








def export_customer_data():
    database_connection = None
    cursor = None
    contacts = []

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.callproc('ExportCustomerData')
        for result in cursor.stored_results():
            contacts.extend(result.fetchall())
    except Exception as e:
        raise Exception(f"An error occurred while fetching customer data: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return contacts








def upload_file(filename, filepath, mimetype, SCOPES=SCOPES):
    """Uploads a file to Google Drive."""
    creds = None
    token_str = os.environ.get('GOOGLE_OAUTH_TOKEN')
    
    # If the token environment variable exists, use it to create credentials
    if token_str:
        token_info = json.loads(token_str)
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
    
    # Check if credentials are valid, otherwise refresh or log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Assuming client secrets are also stored in an environment variable
            client_secrets_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
            flow = InstalledAppFlow.from_client_config(client_secrets_info, SCOPES)
            creds = flow.run_local_server(port=0)
            # Here, you would need to update the environment variable or use a more persistent storage
            # since changes to environment variables in runtime are not persistent across deploys/restarts in Heroku
            
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API to upload the file
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return file.get('id')








def get_google_drive_service():
    """Returns a service object connected to the Google Drive API."""
    creds = None
    # Try to load the token from an environment variable
    token_str = os.environ.get('GOOGLE_OAUTH_TOKEN')
    
    if token_str:
        # If the token was found in the environment variable, load it
        token_info = json.loads(token_str)
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
    
    # Check if the credentials are not valid or do not exist
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Load client secrets from an environment variable
            client_secrets_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
            flow = InstalledAppFlow.from_client_config(client_secrets_info, SCOPES)
            creds = flow.run_local_server(port=0)
            # Note: In a production environment, especially in platforms like Heroku,
            # you should consider a more persistent solution for storing refreshed tokens

    # Build the service object for the Google Drive API
    service = build('drive', 'v3', credentials=creds)
    return service








def generate_shareable_link(file_id):
    service = get_google_drive_service()
    request = service.files().get(fileId=file_id, fields='webViewLink')
    response = request.execute()
    print(f"WebViewLink: {response.get('webViewLink')}")
    return response.get('webViewLink')







def make_file_public(file_id):
    service = get_google_drive_service()
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(
        fileId=file_id,
        body=permission,
        fields='id',
    ).execute()








def get_download_link(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"
    





