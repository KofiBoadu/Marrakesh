
from  .models import create_database_connection
import logging
from app.emails import all_emails_sent_to_customer
from app.customer_notes import get_customer_notes





# def update_customerDetails(contact_id, first_name, last_name, email, phone, gender, state):
#     query = """
#         UPDATE contacts
#         SET first_name = %s,
#             last_name = %s,
#             state_address = %s,
#             email_address = %s,
#             phone_number = %s,
#             gender = %s
#         WHERE contact_id = %s
#     """
#     values = (first_name, last_name, state, email, phone, gender, contact_id)

#     try:
#         database_connection = create_databaseConnection()
#         if database_connection is not None:
#             cursor = database_connection.cursor()
#             cursor.execute(query, values)
#             database_connection.commit()
#             if cursor.rowcount > 0:
#                 print("Customer details successfully updated for ID:", contact_id)
#             else:
#                 print("No customer found with ID:", customer_id)
#     except Error as e:
#         print(f"Database error occurred: {e}")
#         if database_connection:
#             database_connection.rollback()
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()

def update_customerDetails(contact_id, first_name, last_name, email, phone, gender, state):
    query = """
        UPDATE contacts
        SET first_name = %s,
            last_name = %s,
            state_address = %s,
            email_address = %s,
            phone_number = %s,
            gender = %s
        WHERE contact_id = %s
    """
    values = (first_name, last_name, state, email, phone, gender, contact_id)

    try:
        database_connection = create_database_connection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            if cursor.rowcount > 0:
                print("Customer details successfully updated for ID:", contact_id)
            else:
                print("No customer found with ID:", contact_id)
    except Error as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()










def get_customer_booking_changes(contact_id):
    """
    Fetches booking changes for a given customer, including the user names and tour names for old and new tours.

    Parameters:
    - customer_id (int): The ID of the customer whose booking changes are to be fetched.

    Returns:
    - List of tuples containing the booking changes with user names and tour names.
    - Returns an empty list if no changes are found or in case of an error.
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
        logging.error(f"Error in get_customer_booking_changes for customer ID {contact_id}: {e}")
        return []  # Returning an empty list for uniformity
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()







def campaigns_sent_to_customer(contact_id):
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
        cursor.execute(query, (contact_id,contact_id))
        results = cursor.fetchall()
        return results
    except Exception as e:
        logging.error(f"Error in campaigns_sent_to_customer for customer ID {contact_id}: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()



# print(campaigns_sent_to_customer(326))




# def get_customer_activities(customer_id):
#     emails = all_emails_sent_to_customer(customer_id)
#     notes_raw = get_customer_notes(customer_id)
#     booking_changes_raw = get_customer_booking_changes(customer_id)


#     notes = [{'email_id': note[0],
#               'subject': 'Note',
#               'status': '',
#               'sent_date': note[2],
#               'body': note[1],
#               'sent_user': note[3],
#               'is_note': True}
#              for note in notes_raw]


#     booking_changes = [{'email_id': None,
#                         'subject': 'Booking Update',
#                         'status': '',
#                         'sent_date': change[3],
#                         'body': change[4],
#                         'sent_user': change[2],
#                         'is_note': False,
#                         'old_tour_name': change[0],
#                         'new_tour_name': change[1]}
#                        for change in booking_changes_raw]


#     activities = emails + notes + booking_changes

#     activities_sorted = sorted(activities, key=lambda x: x['sent_date'], reverse=True)

#     return activities_sorted

# print(get_customer_activities(326))

def get_customer_activities(contact_id):
    emails = all_emails_sent_to_customer(contact_id)
    notes_raw = get_customer_notes(contact_id)
    booking_changes_raw = get_customer_booking_changes(contact_id)
    campaigns_raw = campaigns_sent_to_customer(contact_id)

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


    activities = emails + notes + booking_changes + campaigns

    activities_sorted = sorted(activities, key=lambda x: x['sent_date'], reverse=True)

    return activities_sorted



# print(get_customer_activities(326))




def update_tour_bookings(tour_id, contact_id):
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






def fetch_customer_details(contact_id):
    query = """SELECT
                c.contact_id,
                c.first_name, 
                c.last_name,
                c.state_address,
                c.email_address,
                c.phone_number
              FROM
                contacts c
              WHERE c.contact_id = %s;"""  # Assuming you're using a placeholder for a parameterized query

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))  # Pass customer_id as a tuple
        customer_data = cursor.fetchall()  # Fetch all rows returned by the query
        return customer_data
    except Exception as e:
        print(f"Database error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




  



def update_customer_email(contact_email,contact_id):
    query = "UPDATE contacts SET email_address = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query,(contact_email, contact_id))
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






def update_contact_phone(contact_id,phone):
    query = "UPDATE contacts SET phone_number = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection=create_database_connection()
        cursor=database_connection.cursor()
        cursor.execute(query, (phone,contact_id))
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








def updating_contact_state(state,contact_id):
    query = "UPDATE contacts SET state_address = %s WHERE contact_id = %s"
    database_connection = None
    try:
        # Assume create_databaseConnection() is a function that establishes a database connection
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (state, contact_id))
        database_connection.commit()

        # Check if the query affected any rows
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
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def updating_contact_status(new_status,contact_id):
    query = "UPDATE contacts SET lead_status = %s WHERE contact_id = %s"
    database_connection = None
    cursor=None
    try:
        # Assume create_databaseConnection() is a function that establishes a database connection
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (new_status,contact_id))
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


   








def update_customer_name(first_name, last_name,contact_id):
    query = "UPDATE contacts SET first_name = %s, last_name = %s WHERE contact_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection=create_database_connection()
        cursor=database_connection.cursor()
        cursor.execute(query, (first_name,last_name,contact_id))
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






def change_customer_bookings(booking_id, new_tour_id, contact_id):
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











def bookings_updates_logs(old_tourID, new_tourID, contactID, updated_by_userID, update_details):
    query = "INSERT INTO booking_updates (old_tour_id, new_tour_id, contact_id, updated_by_user_id, update_details) VALUES (%s, %s, %s, %s, %s)"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (old_tourID, new_tourID, contactID, updated_by_userID, update_details))
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


