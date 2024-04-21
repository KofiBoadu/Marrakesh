from datetime import datetime, timedelta
import pytz
from datetime import datetime, timedelta
from .database import create_database_connection
from tzlocal import get_localzone
from flask_apscheduler import APScheduler
import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from app.users.tour_packages import get_all_tours_scheduled

load_dotenv()


# print(get_all_tours_scheduled())


def add_business_days(start_date, add_days):
    business_days_to_add = add_days
    current_date = start_date
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  
            business_days_to_add -= 1
    return current_date





def generate_due_dates():
    local_tz = get_localzone()
    now = datetime.now(local_tz)  
    tomorrow = now + timedelta(days=1)
    two_business_days = add_business_days(tomorrow, 1)  
    three_business_days = add_business_days(tomorrow, 2)  
    dates = {
        "Today": {"date": now.strftime('%Y-%m-%d'), "day": now.strftime('%A')},
        "Tomorrow": {"date": tomorrow.strftime('%Y-%m-%d'), "day": tomorrow.strftime('%A')},
        "2 Business Days": {"date": two_business_days.strftime('%Y-%m-%d'), "day": two_business_days.strftime('%A')},
        "3 Business Days": {"date": three_business_days.strftime('%Y-%m-%d'), "day": three_business_days.strftime('%A')},
        "1 Week": {"date": (now + timedelta(weeks=1)).strftime('%Y-%m-%d'), "day": (now + timedelta(weeks=1)).strftime('%A')},
        "2 Weeks": {"date": (now + timedelta(weeks=2)).strftime('%Y-%m-%d'), "day": (now + timedelta(weeks=2)).strftime('%A')},
        "1 Month": {"date": (now + timedelta(weeks=4)).strftime('%Y-%m-%d'), "day": (now + timedelta(weeks=4)).strftime('%A')},
        "2 Months": {"date": (now + timedelta(weeks=8)).strftime('%Y-%m-%d'), "day": (now + timedelta(weeks=8)).strftime('%A')},
        "3 Months": {"date": (now + timedelta(weeks=12)).strftime('%Y-%m-%d'), "day": (now + timedelta(weeks=12)).strftime('%A')},
        "6 Months": {"date": (now + timedelta(weeks=24)).strftime('%Y-%m-%d'), "day": (now + timedelta(weeks=24)).strftime('%A')},
        "Custom Date": {"date": None, "day": None}
    }
    return dates




def generate_time_intervals():
    base_time = datetime.strptime('00:00', '%H:%M')
    intervals = []
    for i in range(96):  # 24 hours * 4 intervals per hour
        time_obj = base_time + timedelta(minutes=15 * i)
        display_time = time_obj.strftime('%I:%M %p').lstrip('0')  # Stripping leading zero for 12-hour format with AM/PM
        time_key = time_obj.strftime('%H:%M')  # 24-hour format for backend usage
        intervals.append({'key': time_key, 'value': display_time})
    return intervals






def adding_new_task(task_title, due_date, due_time, description, contact_id,user_id):
    query = "INSERT INTO task (title, due_date, due_time, description, status, contact_id,user_id) VALUES (%s, %s, %s, %s, 'pending', %s,%s)"
    cursor = None
    database_connection = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (task_title, due_date, due_time, description, contact_id,user_id))
        database_connection.commit()
    except Exception as e:
        if database_connection:
            database_connection.rollback()
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()










def check_due_tasks():
    database_connection = create_database_connection()
    cursor = None
    local_tz = pytz.timezone('America/Chicago')  # Adjust timezone as necessary
    now = datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S') 
    
    # print(now) # Local time in properly formatted string
    
    try:
        cursor = database_connection.cursor(dictionary=True)
        query = """
            SELECT t.task_id, t.title, t.due_date, t.due_time, t.description, t.status,
                   c.first_name AS contact_first_name, c.last_name AS contact_last_name, c.email_address AS contact_email, c.phone_number,
                   u.first_name AS user_first_name, u.last_name AS user_last_name, u.email_address AS user_email
            FROM task t
            INNER JOIN contacts c ON t.contact_id = c.contact_id
            INNER JOIN users u ON t.user_id = u.user_id
            WHERE TIMESTAMP(t.due_date, t.due_time) <= %s
            AND t.status = 'pending'
        """

        cursor.execute(query, (now,))
    
        due_tasks = cursor.fetchall()
        return due_tasks

    except Exception as e:
        print(f"Failed to retrieve due tasks: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    
# print(check_due_tasks())



def update_task_status(task_id,new_status):
    database_connection = create_database_connection()
    cursor = None
    try:
        cursor = database_connection.cursor()
        cursor.execute("UPDATE task SET status = %s WHERE task_id = %s", (new_status, task_id))
        database_connection.commit()
    except Exception as e:
        print(f"Failed to update status for task ID {task_id}: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()











def send_task_reminder(task):
    aws_region = os.getenv("REGION", "us-east-2")
    ses_client = boto3.client('ses', region_name=aws_region)
    subject = f"Reminder: Task '{task['title']}' Due Today"
    
    # Directly using HTML with Python f-strings for content insertion
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f4f4f4; /* Light grey background */
      margin: 0;
      padding: 0;
    }}
    .container {{
      background-color: #fff; /* White background for the content container */
      margin: 20px auto;
     
    }}
    .header {{
      font-size: 24px;
      color: #fff; /* White color for text */
      background-color: #03989E; /* Teal-like blue color */
      padding: 10px;
      border-radius: 5px 5px 0 0;
    }}
    .content {{
      font-size: 16px;
      color: #666; /* Dark grey text */
      margin-top: 10px;
    }}
    .note_description {{
      font-size: 18px;
      display: flex;
      justify-content: center;
      padding-top: 10px;
      border-top: 1px solid #ddd; /* Light grey border */
      border-radius: 0 0 5px 5px;
      color: red;
      display: {'none' if not task.get('description') else 'flex'};
    }}
    .contact-info {{
      font-size: 20px;
      padding-top: 50px;
      display: flex;
      justify-content: center;
    }}
    .task_button {{
      display: flex;
      justify-content: center;
      margin-top: 60px;
    }}
    .task_button button {{
      background-color: #FF914C;
      width: 130px;
      padding: 10px;
      margin: 20px;
      color: #fff;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }}
    .footer {{
      font-size: 12px;
      text-align: center;
      margin-top: 20px;
      padding-top: 10px;
      border-top: 1px solid #ddd;
      margin-bottom: 10px;
    }}
  </style>
</head>
<body>
<div class="container">
  <div class="header">
    <h2> Hi, {task['user_first_name']} {task['user_last_name']}</h2>
  </div>
  <div class="content">
    <h2>Your task "{task['title']}" is due today</h2>
  </div>
  <div class="note_description">
    <div id="note-info">
      <p>{task.get('description', ' ')}</p>
    </div>
  </div>
  <div class="contact-info">
    <div id="task-contact">
      <strong>CONTACT</strong><br>
      {task['contact_first_name']} {task['contact_last_name']}<br>
      <a href="mailto:{task['contact_email']}">{task['contact_email']}</a><br>
      {task['phone_number']}
    </div>
  </div>
  <div class="task_button">
    <div id="view-task">
      <button>view task</button>
    </div>
  </div>
  <div class="footer">
    This is an automated task reminder.
  </div>
</div>
</body>
</html>
    """
    
    text_body = f"Hello {task['user_email']}, just a reminder that the task '{task['title']}' is due today."

    try:
        response = ses_client.send_email(
            Source=os.getenv("SENDER_EMAIL"),
            Destination={'ToAddresses': [task['user_email']]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Html': {'Data': html_body},
                    'Text': {'Data': text_body}
                }
            },
            Tags=[{'Name': 'task_id', 'Value': str(task['task_id'])}],
            ConfigurationSetName='sendingTaskreminders'
        )
        print(f"Email sent successfully to {task['user_email']}. Message ID: {response['MessageId']}")
        return True 
    except ClientError as e:
        print(f"Failed to send email to {task['user_email']}: {e.response['Error']['Message']}")
        return False





def schedule_task_reminders():
    try:
        due_tasks = check_due_tasks()
        if due_tasks:
            for task in due_tasks:
                task_id = task["task_id"]
                try:
                    reminder_sent = send_task_reminder(task)
                    if reminder_sent:
                        update_task_status(task_id, "completed")
                        print(f"Reminder sent and status updated for task ID: {task_id}")
                    else:
                        print(f"Failed to send reminder for task ID: {task_id}")
                except Exception as e:
                    print(f"Error sending reminder for task ID {task_id}: {e}")
        else:
            print("no due task ")
            return False 
    except Exception as e:
        print(f"Failed to retrieve due tasks: {e}")



# print(schedule_task_reminders())


