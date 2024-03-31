import datetime
import logging
import os
from urllib.parse import urlparse
import mysql.connector
import phonenumbers
from dotenv import load_dotenv

load_dotenv()


def format_phone_number(number, country_code='US'):
    """
        Formats a phone number to the international format based on the specified country code.

        Parameters:
        - number (str): The phone number to format.
        - country_code (str, optional): The ISO country code to which the number belongs. Defaults to 'US'.

        Returns:
        - A string representing the formatted phone number or an empty string if formatting fails.
    """
    if not number:
        return ""
    try:
        user_number = phonenumbers.parse(number, country_code)
        formatted_number = phonenumbers.format_number(user_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return formatted_number
    except phonenumbers.NumberParseException:
        return ""


def all_states():
    """
        Provides a list of US state abbreviations.

        Returns:
        - A list of strings, each being a US state abbreviation.
    """
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return states


def create_database_connection():
    """
        Establishes a database connection using the connection string from environment variables.

        Returns:
        - A database connection object if successful, None otherwise.

        Raises:
        - ValueError: If the DATABASE_URL environment variable is not set.
        - Logs an error message if the connection fails for any other reason.
    """
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


def create_get_customer_tour_details_procedure():
    """
        Creates a stored procedure in the database to fetch customer tour details.

        The procedure supports pagination and optional filtering based on a search query.

        Returns:
        - True if the procedure is successfully created, raises an Exception otherwise.
    """
    procedure_query = """
        CREATE PROCEDURE GetCustomerTourDetails(
IN search_query VARCHAR(255),
IN items_per_page INT,
IN offset INT)
BEGIN
    IF search_query IS NULL OR search_query = '' THEN
        -- Query modified to return all contacts without booking details,
        -- ordering by contact_id in descending order to show recent contacts first
        SELECT DISTINCT
            c.contact_id,
            CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
            c.state_address AS `State`,
            c.email_address AS `Email`,
            c.phone_number AS `Mobile`,
            c.lead_status AS  `Lead Status`
        FROM
            contacts c
        ORDER BY
            c.contact_id DESC
        LIMIT items_per_page OFFSET offset;
    ELSE
        -- Query with enhanced filtering based on search_query
        SELECT DISTINCT
            c.contact_id,
            CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
            c.state_address AS `State`,
            c.email_address AS `Email`,
            c.phone_number AS `Mobile`,
            c.lead_status AS  `Lead Status`
        FROM
            contacts c
        WHERE
            c.first_name LIKE CONCAT('%', search_query, '%') OR
            c.last_name LIKE CONCAT('%', search_query, '%') OR
            CONCAT(c.first_name, ' ', c.last_name) LIKE CONCAT('%', search_query, '%') OR
            c.phone_number LIKE CONCAT('%', search_query, '%') OR
            c.email_address LIKE CONCAT('%', search_query, '%')
        ORDER BY
            c.contact_id DESC
        LIMIT items_per_page OFFSET offset;
    END IF;
END;

    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS GetCustomerTourDetails")
        cursor.execute(procedure_query)
        database_connection.commit()
        return True
    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")

    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


def get_total_num_of_contacts():
    """
        Counts the total number of contacts in the database.

        Returns:
        - The total number of contacts as an integer, or raises an Exception on error.
    """
    cursor = None
    database_connection = None
    query = "SELECT COUNT(*) FROM contacts"
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        raise Exception(f"An error occurred while counting: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def get_all_contacts_information(page=1, items_per_page=25, search_query=''):
    """
        Fetches contact information from the database with optional pagination and search filtering.

        Parameters:
        - page (int, optional): The current page number for pagination.
        - items_per_page (int, optional): The number of items per page for pagination.
        - search_query (str, optional): A search query to filter results.

        Returns:
        - A list of contacts matching the criteria or False if no contacts found. Raises an Exception on error.
    """
    offset = (page - 1) * items_per_page
    database_connection = None
    contacts = []
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.callproc('GetCustomerTourDetails', [search_query, items_per_page, offset])
        for result in cursor.stored_results():
            contacts.extend(result.fetchall())
    except Exception as e:
        raise Exception(f"An error occurred while fetching customer information: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    if len(contacts) == 0:

        return []

    else:

        return contacts


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


def get_contact_id(email):
    """
        Retrieves the contact ID for a given email address.

        Parameters:
        - email (str): The email address of the contact.

        Returns:
        - The contact ID if found, None otherwise.
    """
    query = "SELECT contact_id FROM contacts WHERE email_address = %s"
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logging.error(f"Error in get_customer_id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


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


def add_new_contact(first_name, last_name, email, phone=None, gender=None, state=None, lead_status="Lead"):
    """
        Adds a new contact to the database with specified attributes.

        Parameters:
        - first_name (str): The first name of the contact.
        - last_name (str): The last name of the contact.
        - email (str): The email address of the contact.
        - phone (str, optional): The phone number of the contact.
        - gender (str, optional): The gender of the contact.
        - state (str, optional): The state of the contact.
        - lead_status (str, optional): The lead status of the contact, defaults to "Lead".

        Returns:
        - The ID of the newly added contact if the operation was successful, None otherwise.

        Note:
        - The function commits the new contact information to the database and returns the unique ID assigned to the contact.
    """
    query = """
        INSERT INTO contacts
        (first_name, last_name, state_address, email_address, phone_number, gender, lead_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    database_connection = None
    cursor = None
    values = (first_name, last_name, state, email, phone, gender, lead_status)
    try:
        database_connection = create_database_connection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            print("Customer successfully added with ID:", cursor.lastrowid)
            return cursor.lastrowid  # Return the new contact's ID
    except Exception as e:  # Catch a more general exception
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
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


def check_contact_exists(email):
    """
        Checks if a contact already exists in the database based on their email address.

        Parameters:
        - email (str): The email address of the contact to check.

        Returns:
        - The ID of the contact if they exist, None otherwise.

        Note:
        - This function is useful for avoiding duplicate entries in the database.
    """
    query = "SELECT contact_id FROM contacts WHERE TRIM(LOWER(email_address)) = TRIM(LOWER(%s))"
    contact_id = None
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()

        cursor.execute(query, (email,))
        results = cursor.fetchall()

        if len(results) > 1:
            logging.warning(f"Multiple entries found for {email}: {len(results)} entries.")

        if results:
            contact_id = results[0][0]

    except mysql.connector.Error as db_err:
        logging.error(f"Database error occurred: {db_err}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error as err:
                logging.error(f"Error closing cursor: {err}")
        if 'database_connection' in locals() and database_connection is not None:
            try:
                database_connection.close()
            except mysql.connector.Error as err:
                logging.error(f"Error closing connection: {err}")

    return contact_id


def get_total_number_of_travellers():
    """
        Calculates the total number of travellers for the current year.

        Returns:
        - An integer representing the total number of travellers or 0 if none found.

        Note:
        - The calculation is based on bookings for tours starting in the current year.
    """
    target_year = datetime.datetime.now().year
    query = """
        SELECT COUNT(tb.booking_id)
        FROM tour_bookings tb
        JOIN tours t ON tb.tour_id = t.tour_id
        WHERE YEAR(t.start_date) = %s
    """
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        if database_connection:
            cursor = database_connection.cursor()
            cursor.execute(query, (target_year,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0
    except mysql.connector.Error as db_err:
        logging.error(f"Database error occurred: {db_err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return None


def calculate_gross_revenue(year):
    """
        Calculates the gross revenue generated from tour bookings in a given year.

        Parameters:
        - year (int): The year for which to calculate gross revenue.

        Returns:
        - A formatted string representing the total revenue and the revenue as a float.

        Note:
        - The revenue is calculated as the sum of prices for all booked tours starting in the specified year.
    """
    query = """
        SELECT COALESCE(SUM(t.tour_price), 0) AS total_revenue
        FROM tour_bookings tb
        JOIN tours t ON tb.tour_id = t.tour_id
        WHERE YEAR(t.start_date) = %s
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (year,))
        result = cursor.fetchone()
        total_revenue = result[0] if result else 0
        revenue = float(total_revenue)
        upper = int(revenue / 1000)
        middle = int(revenue - upper * 1000)
        lower = int(revenue * 100 - upper * 100000 - middle * 100)
        if upper == 0:
            format_rev = f"{middle}.{lower}"

        else:
            format_rev = f"{upper},{middle}.{lower}"

        return format_rev, revenue


    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def remove_a_paid_contact(contact_id):
    """
        Deletes a contact from the database, typically after their account has been settled or closed.

        Parameters:
        - contact_id (int): The ID of the contact to remove.

        Returns:
        - True if the contact was successfully deleted, False otherwise.

        Note:
        - This operation is transactional and will be rolled back if any error occurs during execution.
    """
    deleted = False
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        database_connection.autocommit = False
        cursor = database_connection.cursor()
        cursor.execute("DELETE FROM contacts WHERE contact_id=%s", (contact_id,))
        customer_deleted = cursor.rowcount > 0
        if customer_deleted:
            database_connection.commit()
            deleted = True
        else:
            database_connection.rollback()
        cursor.close()
    except Exception as e:
        logging.error(f"An error occurred while deleting customer: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()
    return deleted
