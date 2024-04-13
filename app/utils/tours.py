from .database import create_database_connection
import mysql.connector
import logging
from datetime import datetime




def get_travel_package_id(tour_name, year):
    """
        Retrieves the ID of a travel package based on the tour name and year.

        Parameters:
        - tour_name (str): The name of the tour.
        - year (int): The year of the tour.

        Returns:
        - The ID of the matching tour package if found, None otherwise.
    """
    query = "SELECT tour_id FROM tours WHERE TRIM(tour_name) = %s and YEAR(start_date) = %s"

    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (tour_name, year))
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as e:
        # Handle specific database errors here
        logging.error(f"Database error in get_travel_package_id: {e}")
        return None
    except Exception as e:
        # Handle general errors here
        logging.error(f"Error in get_travel_package_id: {e}")
        return None
    finally:
        if database_connection:
            database_connection.close()
        if cursor:
            cursor.close()




def create_new_tour_packages(tour_name, start_date, end_date, price, destination_id, tour_type):
    """
        Creates a new tour package in the database.

        Parameters:
        - tour_name (str): Name of the tour.
        - start_date (date): Start date of the tour.
        - end_date (date): End date of the tour.
        - price (float): Price of the tour.
        - destination_id (int): ID of the destination.
        - tour_type (str): Type of the tour.

        Returns:
        - True if the new tour package was successfully created, False otherwise.
    """
    query = ("INSERT INTO tours(tour_name, start_date, end_date, tour_price, destination_id, tour_type) VALUES(%s, %s, "
             "%s, %s, %s, %s)")
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (tour_name, start_date, end_date, price, destination_id, tour_type))
        database_connection.commit()
        return True
    except mysql.connector.Error as e:
        logging.error(f"Database error in create_new_tour_packages: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    except Exception as e:
        logging.error(f"Error in create_new_tour_packages: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def get_all_destinations():
    """
        Retrieves a list of all destination names from the database.

        Returns:
        - A list of destination names as strings.

        Note:
        - This function is useful for populating destination options in user interfaces or reports.
    """
    query = "SELECT destination_name FROM destinations"
    destinations = []
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        if database_connection:
            cursor = database_connection.cursor()
            cursor.execute(query)
            destination_tuples = cursor.fetchall()
            destinations = [destination[0] for destination in destination_tuples]
        else:
            logging.error("Failed to connect to the database")

    except Exception as e:
        destinations = []

    finally:

        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return destinations




def get_destination_id(destination_name):
    """
        Fetches the unique ID of a destination based on its name.

        Parameters:
        - destination_name (str): The name of the destination.

        Returns:
        - The destination ID if found, None otherwise.

        Note:
        - This function is case-insensitive and capitalizes the destination name for matching in the database.
    """
    destination = destination_name.capitalize()
    query = "SELECT destination_id FROM destinations WHERE destination_name = %s"
    database_connection = create_database_connection()
    cursor = database_connection.cursor()
    cursor.execute(query, (destination,))
    result = cursor.fetchone()
    cursor.close()
    database_connection.close()
    if result:
        return result[0]
    else:
        return None



def get_all_upcoming_travel_packages():
    """
        Fetches all upcoming travel packages sorted by proximity to the current date.

        Returns:
        - A list of upcoming travel packages by name and year, or an empty list if an error occurs.
    """
    current_year = datetime.date.today().year
    query = """
    SELECT Concat(tour_name, " ", YEAR(t.start_date))
    FROM tours t
    WHERE YEAR(t.start_date) >= %s
    ORDER BY ABS(YEAR(start_date) - YEAR(CURDATE())) ASC, start_date DESC;"""
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (current_year,))
        date_tuples = cursor.fetchall()
        dates = [date[0] for date in date_tuples]
        return dates
    except Exception as e:
        logging.error(f"Error in get_all_upcoming_travel_packages: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def book_a_tour_for_a_contact(tour_id, contact_id):
    """
        Books a tour for a specific contact.

        Parameters:
        - tour_id (int): The ID of the tour to be booked.
        - contact_id (int): The ID of the contact booking the tour.

        Returns:
        - True if the booking was successful, False otherwise.
    """
    query = "INSERT INTO tour_bookings(tour_id, contact_id) VALUES(%s, %s)"
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (tour_id, contact_id))
        database_connection.commit()
        return True
    except Exception as e:
        logging.error(f"Error in book_a_tour_for_a_contact: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()