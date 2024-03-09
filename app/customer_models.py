
from  .models import create_databaseConnection
import logging

from app.emails import all_emails_sent_to_customer
from app.customer_notes import get_customer_notes





def update_customerDetails(customer_id, first_name, last_name, email, phone, gender, state):
    query = """
        UPDATE customers
        SET first_name = %s,
            last_name = %s,
            state_address = %s,
            email_address = %s,
            phone_number = %s,
            gender = %s
        WHERE customer_id = %s
    """
    values = (first_name, last_name, state, email, phone, gender, customer_id)

    try:
        database_connection = create_databaseConnection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            if cursor.rowcount > 0:
                print("Customer details successfully updated for ID:", customer_id)
            else:
                print("No customer found with ID:", customer_id)
    except Error as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()







def get_customer_activities(customer_id):
    emails = all_emails_sent_to_customer(customer_id)
    notes_raw = get_customer_notes(customer_id)
    
    # Convert notes to the same dictionary format as emails for uniform handling
    notes = [{'email_id': note[0], 
              'subject': 'Note', 
              'status': '', 
              'sent_date': note[2], 
              'body': note[1],  # note_message is assigned to body
              'sent_user': note[3],  # Assuming index 3 is the sent_user in your notes_raw tuple
              'is_note': True}  # Differentiate notes from emails
             for note in notes_raw]

    # Combine emails and notes
    activities = emails + notes

    # Sort by 'sent_date'
    activities_sorted = sorted(activities, key=lambda x: x['sent_date'], reverse=True)

    return activities_sorted




def update_tour_bookings(tour_id, customer_id):
    query = "UPDATE tour_bookings SET tour_id = %s WHERE customer_id = %s"
    database_connection = None
    cursor = None

    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (tour_id, customer_id))
        database_connection.commit()
        if cursor.rowcount > 0:
            print(f"Successfully updated tour_id for customer_id {customer_id}")
            return True
        else:
            print(f"No record found to update for customer_id {customer_id}")
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






def fetch_customer_details(customer_id):
    query = """SELECT
                c.customer_id,
                c.first_name, 
                c.last_name,
                c.state_address,
                c.email_address,
                c.phone_number
              FROM
                customers c
              WHERE c.customer_id = %s;"""  # Assuming you're using a placeholder for a parameterized query

    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (customer_id,))  # Pass customer_id as a tuple
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




  



def update_customer_email(customer_email,customer_id):
    query = "UPDATE customers SET email_address = %s WHERE customer_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query,(customer_email, customer_id))
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






def update_customer_phone(customer_id,phone):
    query = "UPDATE customers SET phone_number = %s WHERE customer_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection=create_databaseConnection()
        cursor=database_connection.cursor()
        cursor.execute(query, (customer_id,phone))
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








def updating_customer_state(state,customer_id):
    query = "UPDATE customers SET state_address = %s WHERE customer_id = %s"
    database_connection = None
    try:
        # Assume create_databaseConnection() is a function that establishes a database connection
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (state, customer_id))
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




   








def update_customer_name(first_name, last_name,customer_id):
    query = "UPDATE customers SET first_name = %s, last_name = %s WHERE customer_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection=create_databaseConnection()
        cursor=database_connection.cursor()
        cursor.execute(query, (first_name,last_name,customer_id))
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






def change_customer_bookings(booking_id, new_tour_id, customer_id):
    """
    Updates the tour_id for a given booking and customer.

    Parameters:
    - booking_id: The ID of the booking to update.
    - new_tour_id: The new tour ID to associate with the booking.
    - customer_id: The ID of the customer who made the booking.

    Returns:
    - True if the update was successful, False otherwise.
    """
    query = "UPDATE tour_bookings SET tour_id = %s WHERE booking_id = %s AND customer_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (new_tour_id, booking_id, customer_id))
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











def bookings_updates_logs(old_tourID, new_tourID, customerID, updated_by_userID, update_details):
    query = "INSERT INTO booking_updates (old_tour_id, new_tour_id, customer_id, updated_by_user_id, update_details) VALUES (%s, %s, %s, %s, %s)"
    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (old_tourID, new_tourID, customerID, updated_by_userID, update_details))
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


