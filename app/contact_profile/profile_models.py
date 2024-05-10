import logging
from app.utils.database import create_database_connection
from datetime import datetime, timedelta
from itertools import groupby


#
# known_fields = {
#     'message',
#     'how_many_travelers',
#     'enter_full_names_and_emails__of_other_travelers_if_any',
#     'what_type_of_tour',
#     'referral_name_or_code_if_any',
#     'how_did_you_hear_about_us',
#     'city',
#     'postal_/_zip_code',
#     'country',
#     'type_of_accommodation',
#     'payment_options',
#     'address',
#     'what_is_the_best_way_to_contact_you',
#     'if_phone_when_is_the_best_time_of_day_for_a_call_back',
#     'is_there_anything_else_we_should_know',
#     'deposit_amount',
#     'date',
#     'time',
#     'page_url',
#     'form_name',
#     "Accommodation Type",
#     "Budget (Budget Excluding Flights)",
#     " Destination",
#     "Message",
#     "Time",
#     " What Is The Best Way To Contact You?",
#     'Are you prepared to secure your spot with a deposit within the next week?'
#
# }


def profile_details(contact_id):
    query = """
        SELECT
          CONCAT(c.first_name, ' ', c.last_name) AS full_name,
          c.email_address,
          c.phone_number,
          c.state_address,
          c.lead_status,
          c.gender,
          COALESCE(GROUP_CONCAT(CONCAT(t.tour_type, " ", t.tour_name, ' ', YEAR(t.start_date)) SEPARATOR ', '), '') AS tour_details,
          COALESCE(SUM(t.tour_price), 0) AS total_tour_price
        FROM
          contacts c
        LEFT JOIN
          tour_bookings tb ON c.contact_id = tb.contact_id
        LEFT JOIN
          tours t ON tb.tour_id = t.tour_id
        WHERE
          c.contact_id = %s
        GROUP BY
          c.contact_id;
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        if results and results[0]:
            return results[0]
        else:
            # Handle case where the contact exists but has no bookings
            cursor.execute(
                "SELECT CONCAT(first_name, ' ', last_name) AS full_name, email_address, phone_number, state_address, "
                "lead_status, gender FROM contacts WHERE contact_id = %s",
                (contact_id,))
            results = cursor.fetchall()
            return results[0] + ('', 0) if results else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


def get_customer_bookings(contact_id):
    query = """
        SELECT
            tb.booking_id,
            tb.tour_id,
            tb.contact_id,
            GROUP_CONCAT(CONCAT(t.tour_name, ' ', YEAR(t.start_date)) SEPARATOR ', ') AS tour_details
        FROM
            tour_bookings tb
        JOIN tours t ON tb.tour_id = t.tour_id
        WHERE
            tb.contact_id = %s
        GROUP BY
            tb.booking_id, tb.tour_id, tb.contact_id;
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        # Convert results to a list of dictionaries
        bookings = [
            {"booking_id": row[0], "tour_id": row[1], "contact_id": row[2], "tour_name": row[3]}
            for row in results
        ]
        return bookings if bookings else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


def contact_gender_update(contact_id, gender):
    query = """
    UPDATE contacts
    SET gender = %s
    WHERE contact_id = %s;
    """
    cursor = None
    database_connection = None
    try:

        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (gender, contact_id))

        database_connection.commit()
    except Exception as e:

        print(f"An error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:

        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def contact_submissions(contact_id):
    query = """

        SELECT
            c.first_name,
            c.last_name,
            fs.submission_source,
            fs.submission_date,
            fd.field_name,
            fd.field_value
        FROM contacts c
        JOIN form_submissions fs ON fs.contact_id = c.contact_id
        JOIN form_data fd ON fd.submission_id = fs.submission_id
        WHERE c.contact_id = %s;

    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        return results if results else None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


def all_emails_sent_to_contacts(contact_id):
    """
        Retrieves all emails sent to a specific contact, ordered by the most recent.

        Parameters:
        - contact_id (int): The ID of the contact whose emails are to be retrieved.

        Returns:
        - list: A list of dictionaries, each representing an email sent to the contact. Includes email ID, subject, status, sent date, body, and the user who sent the email.

        Note:
        - Handles database exceptions by printing an error message but returns an empty list in such cases to ensure the function always returns a list.
    """
    database_connection = None
    cursor = None
    query = ("SELECT email_id, subject, status, sent_date, body, sent_user FROM emails WHERE contact_id = %s ORDER BY "
             "email_id DESC")
    all_emails = []
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        all_emails = [
            {'email_id': email[0], 'subject': "Email " + email[1], 'status': email[2], 'sent_date': email[3],
             'body': email[4],
             "sent_user": email[5]} for email in results]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()
    return all_emails


def save_contact_notes(contact_id, note_message, note_creator):
    """
        Inserts a new note into the database for a specified contact.

        This function saves a note message associated with a contact ID into the database. It records who created the note and timestamps the entry automatically.

        Parameters:
        - contact_id (int): The ID of the contact for whom the note is being saved.
        - note_message (str): The content of the note being saved.
        - note_creator (str): Identifier (such as a username or ID) of the person or system that created the note.

        Raises:
        - Exception: If an error occurs during the database operation, an exception is raised with details of the error.

        Note:
        - The function attempts to open a database connection, execute the insert operation, and commit the changes. If an error occurs, it raises an exception with the error message. The database connection is always closed before the function exits, regardless of whether an error occurred.
    """
    database_connection = None
    cursor = None
    query = "INSERT INTO notes (contact_id, note_message, note_creator) VALUES (%s, %s, %s)"
    values = (contact_id, note_message, note_creator)

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, values)
        database_connection.commit()

    except Exception as e:
        raise Exception(f"An error occurred while saving customer notes: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


def get_contacts_notes(contact_id):
    """
        Retrieves all notes from the database associated with a specified contact ID.

        This function queries the database for notes related to a given contact, ordered by the note creation date in descending order, ensuring the most recent notes are returned first.

        Parameters:
        - contact_id (int): The ID of the contact whose notes are to be retrieved.

        Returns:
        - list: A list of tuples, each representing a note associated with the contact. Each tuple contains the note's ID, message, creation date, and creator. Returns an empty list if no notes are found or an error occurs.

        Note:
        - In case of a database error, the function will print an error message but will return an empty list to ensure the calling code can continue execution without handling exceptions.
    """
    database_connection = None
    cursor = None
    query = ("SELECT notes_id, note_message, date_created, note_creator FROM notes WHERE contact_id = %s ORDER BY "
             "notes_id DESC")

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()

    except Exception as e:
        print(f"An error occurred: {e}")
        results = []  # Ensure that results is always a list, even after an exception.
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return results


def delete_contacts_notes(notes_id, contact_id):
    """
        Deletes a specific note for a contact from the database.

        This function removes a note identified by its ID and associated with a given contact ID. It ensures that only notes belonging to the specified contact can be deleted.

        Parameters:
        - notes_id (int): The ID of the note to be deleted.
        - contact_id (int): The ID of the contact associated with the note.

        Note:
        - If an error occurs during the deletion process, an error message is printed and any changes are rolled back. The function ensures that the database connection is properly closed before exiting.

        Raises:
        - Prints an error message if the deletion operation fails due to a database error. Includes rollback of the transaction to ensure database integrity.
    """
    database_connection = None
    cursor = None
    query = "DELETE FROM notes WHERE notes_id = %s AND contact_id = %s"
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (notes_id, contact_id))
        database_connection.commit()
    except Exception as e:
        print(f"An error occurred while deleting the note: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def update_contact_email(contact_email, contact_id):
    """
        Updates the email address for a specific contact in the database.

        Parameters:
        - contact_email (str): The new email address for the contact.
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - True if the update was successful, False otherwise.
    """
    query = "UPDATE contacts SET email_address = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_email, contact_id))
        database_connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error in update_tour_bookings: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def update_contact_phone(contact_id, phone):
    """
        Updates the phone number for a specific contact in the database.

        Parameters:
        - contact_id (int): Unique identifier for the contact.
        - phone (str): The new phone number for the contact.

        Returns:
        - True if the update was successful, False otherwise.
    """
    query = "UPDATE contacts SET phone_number = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (phone, contact_id))
        database_connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error in updating name : {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def updating_contact_state(state, contact_id):
    """
        Updates the state address for a specific contact in the database.

        Parameters:
        - state (str): The new state address for the contact.
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - True if the update was successful, False otherwise.
    """
    query = "UPDATE contacts SET state_address = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (state, contact_id))
        database_connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        # Log the exception if an error occurs
        logging.error(f"Error in updating customer state: {e}")
        if database_connection:
            database_connection.rollback()
        return False

    finally:

        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def updating_contact_status(new_status, contact_id):
    """
        Updates the lead status for a specific contact in the database.

        Parameters:
        - new_status (str): The new lead status for the contact.
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - True if the update was successful, False otherwise.
    """
    query = "UPDATE contacts SET lead_status = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:

        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (new_status, contact_id))
        database_connection.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:

        logging.error(f"Error in updating customer state: {e}")
        if database_connection:
            database_connection.rollback()
        return False

    finally:

        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def update_contact_name(first_name, last_name, contact_id):
    """
        Updates the name (first and last) for a specific contact in the database.

        Parameters:
        - first_name (str): The new first name for the contact.
        - last_name (str): The new last name for the contact.
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - True if the update was successful, False otherwise.
    """
    query = "UPDATE contacts SET first_name = %s, last_name = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (first_name, last_name, contact_id))
        database_connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error in updating name : {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def change_contact_bookings(booking_id, new_tour_id, contact_id):
    """
    Updates the tour_id for a given booking and customer.

    Parameters:
    - booking_id: The ID of the booking to update.
    - new_tour_id: The new tour ID to associate with the booking.
    - customer_id: The ID of the customer who made the booking.

    Returns:
    - True if the update was successful, False otherwise.
    """
    query = "UPDATE tour_bookings SET tour_id = %s WHERE booking_id = %s AND contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (new_tour_id, booking_id, contact_id))
        database_connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error in updating booking: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def bookings_updates_logs(old_tour_id, new_tour_id, contact_id, updated_by_user_id, update_details):
    """
        Updates the tour ID for a specific booking to a new tour, effectively changing the tour associated with a booking for a given contact. This function is typically used to accommodate a customer's request to change their tour booking to a different tour offering.

        Parameters:
        - booking_id (int): The ID of the booking that needs to be updated. This is the unique identifier for the specific booking made by the contact.
        - new_tour_id (int): The ID of the new tour to which the booking should be updated. This represents the new tour choice of the contact.
        - contact_id (int): The ID of the contact who made the booking. This ensures that the booking being updated belongs to the correct customer.

        Returns:
        - bool: True if the booking update was successful (i.e., if the specified booking was found and updated with the new tour ID), False otherwise (e.g., if the booking or contact ID does not exist in the database).

        Raises:
        - Logs an error message to a logging service or console if the database update operation fails due to an exception.

        Note:
        - The function also ensures the integrity of the booking by committing the change to the database and rolling back in case of an error to prevent partial updates.
    """
    query = ("INSERT INTO booking_updates (old_tour_id, new_tour_id, contact_id, updated_by_user_id, update_details) "
             "VALUES (%s, %s, %s, %s, %s)")
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (old_tour_id, new_tour_id, contact_id, updated_by_user_id, update_details))
        database_connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error in inserting booking: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def fetch_contact_details(contact_id):
    """
        Fetches the contact details for a specific contact ID from the database.

        Parameters:
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - A list of tuples containing the contact's details, or None in case of an error.
    """
    query = """SELECT
                c.contact_id,
                c.first_name, 
                c.last_name,
                c.state_address,
                c.email_address,
                c.phone_number
              FROM
                contacts c
              WHERE c.contact_id = %s;"""
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        customer_data = cursor.fetchall()
        return customer_data
    except Exception as e:
        print(f"Database error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def all_email_campaigns_sent_to_contact(contact_id):
    """
        Retrieves all email campaigns sent to a specific contact.

        Parameters:
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - A list of tuples with the full name of the contact, campaign ID, subject, sent date, and event type of all email campaigns sent to the contact, or an empty list in case of an error.
    """

    query = """
            SELECT
                CONCAT(c.first_name, ' ', c.last_name) AS full_name,
                e.campaign_id,
                e.campaign_subject,
                e.sent_date,
                m.event_type
            FROM
                (SELECT
                     campaign_id,
                     MAX(metric_id) as latest_metric_id
                 FROM
                     marketing_email_metrics
                 WHERE
                     contact_id = %s
                 GROUP BY
                     campaign_id
                ) AS latest_campaign_metrics
            JOIN
                marketing_email_metrics m ON latest_campaign_metrics.latest_metric_id = m.metric_id
            JOIN
                marketing_emails e ON m.campaign_id = e.campaign_id
            JOIN
                contacts c ON m.contact_id = c.contact_id
            WHERE
                c.contact_id = %s
            ORDER BY
                e.sent_date DESC;
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id, contact_id))
        results = cursor.fetchall()
        return results
    except Exception as e:
        logging.error(f"Error in all_email_campaigns_sent_to_contact for customer ID {contact_id}: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def get_contact_booking_changes(contact_id):
    """
    Fetches booking changes for a given contact ID, including details of the old and new tours and the user who made the update.

    Parameters:
    - contact_id (int): Unique identifier for the contact.

    Returns:
    - A list of tuples containing details of booking changes, or an empty list if no changes are found or in case of an error.
    """

    query = """
    SELECT
        t_old.tour_name AS old_tour_name,
        t_new.tour_name AS new_tour_name,
        CONCAT(u.first_name, ' ', u.last_name) AS updated_by_username,  -- Added space between names
        bu.update_time,
        bu.update_details
    FROM
        booking_updates bu
        JOIN tours t_old ON bu.old_tour_id = t_old.tour_id
        JOIN tours t_new ON bu.new_tour_id = t_new.tour_id
        JOIN users u ON bu.updated_by_user_id = u.user_id
    WHERE
        bu.contact_id = %s
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        return results
    except Exception as e:
        logging.error(f"Error in get_contact_booking_changes for customer ID {contact_id}: {e}")
        return []  # Returning an empty list for uniformity
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def get_contact_activities(contact_id):
    """
        Aggregates all activities related to a specific contact, including emails, notes, booking changes, campaigns, and form submissions.

        Parameters:
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - A sorted list of dictionaries, each representing an activity, sorted by sent date in descending order.
    """
    emails = all_emails_sent_to_contacts(contact_id)
    notes_raw = get_contacts_notes(contact_id)
    booking_changes_raw = get_contact_booking_changes(contact_id)
    campaigns_raw = all_email_campaigns_sent_to_contact(contact_id)
    contact_submissions_raw = contact_submissions(contact_id)

    notes = [{'email_id': note[0],
              'subject': 'Note',
              'status': '',
              'sent_date': note[2],
              'body': note[1],
              'sent_user': note[3],
              'is_note': True}
             for note in notes_raw]
    booking_changes = [{'email_id': None,
                        'subject': 'Booking Update',
                        'status': '',
                        'sent_date': change[3],
                        'body': change[4],
                        'sent_user': change[2],
                        'is_note': False}
                       for change in booking_changes_raw]

    campaigns = [{
        'email_id': campaign[1],
        'subject': campaign[2],
        'status': campaign[4],
        'sent_date': campaign[3],
        'body': f"Event Type: {campaign[4]}",
        'sent_user': 'Campaign System',
        'full_name': campaign[0],
        'is_note': False
    } for campaign in campaigns_raw]

    submissions = []
    if contact_submissions_raw:

        contact_submissions_raw.sort(key=lambda x: x[3])

        for _, group in groupby(contact_submissions_raw, key=lambda x: x[3]):
            grouped_fields = list(group)
            first_entry = grouped_fields[0]

            form_fields = [{'name': entry[4].replace('_', ' ').capitalize(), 'value': entry[5]} for entry in
                           grouped_fields]

            submissions.append({
                'type': 'submission',
                'subject': 'Form Submission via ' + first_entry[2],
                'sent_date': first_entry[3].isoformat(),
                'form_fields': form_fields,
                'sent_user': f"{first_entry[0]} {first_entry[1]}",
            })
    # Combine all activities
    activities = emails + notes + booking_changes + campaigns + submissions
    for activity in activities:
        if isinstance(activity['sent_date'], str):
            activity['sent_date'] = datetime.fromisoformat(activity['sent_date'])
    activities_sorted = sorted(activities, key=lambda x: x['sent_date'], reverse=True)
    return activities_sorted


def update_tour_bookings(tour_id, contact_id):
    """
        Updates the tour ID for a specific booking made by a contact.

        Parameters:
        - tour_id (int): The new tour ID to be associated with the booking.
        - contact_id (int): Unique identifier for the contact.

        Returns:
        - True if the update was successful, False otherwise.
    """
    query = "UPDATE tour_bookings SET tour_id = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (tour_id, contact_id))
        database_connection.commit()
        if cursor.rowcount > 0:
            print(f"Successfully updated tour_id for customer_id {contact_id}")
            return True
        else:
            print(f"No record found to update for customer_id {contact_id}")
            return False
    except Exception as e:
        logging.error(f"Error in update_tour_bookings: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def get_contact_task(contact_id):
    # Corrected SQL query to properly format the CONCAT function and include a space between first and last name
    query = """
    SELECT task.task_id, task.title, task.due_date, task.due_time, task.description, 
           CONCAT(users.first_name, ' ', users.last_name) AS assigned_user
    FROM task
    JOIN users ON users.user_id = task.user_id
    WHERE task.contact_id = %s
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        # Execute the query with the contact_id as a parameter to filter the tasks
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print("An error occurred:", e)
        return []
    finally:
        # Ensure resources are freed by closing the cursor and the database connection
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

# date=get_contact_task(6457)[0][2]
# print(date)


# print(timedelta_to_time_str(timedelta(seconds=9900)))
