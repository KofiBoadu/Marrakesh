import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor, as_completed



load_dotenv()



smtp_settings={
        'server': 'email-smtp.us-east-2.amazonaws.com',
        'port': 587,  
        'username': os.getenv('SES_USERNAME'),
        'password': os.getenv('SES_PASSWORD'),
        'tls': True  
    }


# print(smtp_settings['password'])


def send_email_marketing(customer_name, receiver_email, subject, sender_email, text_body,smtp_settings=smtp_settings):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
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





