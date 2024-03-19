import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import logging
import datetime
import phonenumbers
from phonenumbers import geocoder, carrier
from urllib.parse import urlparse
import datetime


load_dotenv()







def format_phone_number(number, country_code='US'):
    user_number = phonenumbers.parse(number, country_code)
    formatted_number = phonenumbers.format_number(user_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return formatted_number



def all_states():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return states





# def create_databaseConnection():
#     database_url = os.getenv('JAWSDB_URL')
#     if database_url:
#         parsed_url = urlparse(database_url)
#         db_user = parsed_url.username
#         db_password = parsed_url.password
#         db_host = parsed_url.hostname
#         db_name = parsed_url.path.lstrip('/')
#         db_port = parsed_url.port
#         try:
#             sql_connection= mysql.connector.connect(
#                     user=db_user,
#                     password=db_password,
#                     host=db_host,
#                     database=db_name,
#                     port=db_port
#             )
#             return sql_connection

#         except mysql.connector.Error as e:

#             logging.error(f"An error occurred while connecting to the database: {e}")

#     else:
#         logging.error("DATABASE_URL not set")
#         raise ValueError("DATABASE_URL not set")








# def create_get_customer_tour_details_procedure():

#     procedure_query = """
#         CREATE PROCEDURE GetCustomerTourDetails(
#         IN search_query VARCHAR(255),
#         IN items_per_page INT,
#         IN offset INT)
#     BEGIN
#         IF search_query IS NULL OR search_query = '' THEN
#             -- Original query without filtering, modified to include DISTINCT
#             SELECT DISTINCT
#                 c.contact_id,
#                 CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
#                 c.state_address AS `State`,
#                 c.email_address AS `Email`,
#                 c.phone_number AS `Mobile`,
#                 c.lead_status AS  `Lead Status`
             
#             FROM
#                 contacts c
#             JOIN
#                 tour_bookings tb ON tb.contact_id = c.contact_id
#             JOIN
#                 tours t ON tb.tour_id = t.tour_id
#             ORDER BY
#                 YEAR(t.start_date) DESC, c.contact_id DESC
#             LIMIT items_per_page OFFSET offset;
#         ELSE
#             -- Query with filtering based on search_query, modified to include DISTINCT
#             SELECT DISTINCT
#                 c.contact_id,
#                 CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
#                 c.state_address AS `State`,
#                 c.email_address AS `Email`,
#                 c.phone_number AS `Mobile`,
#                 c.lead_status AS  `Lead Status`

#             FROM
#                 contacts c
#             JOIN
#                 tour_bookings tb ON tb.contact_id = c.contact_id
#             JOIN
#                 tours t ON tb.tour_id = t.tour_id
#             WHERE
#                 c.first_name LIKE CONCAT(search_query, '%') OR
#                 CONCAT(c.first_name, ' ', c.last_name) LIKE CONCAT('%', search_query, '%')
#             ORDER BY
#                 YEAR(t.start_date) DESC, c.contact_id DESC
#             LIMIT items_per_page OFFSET offset;
#         END IF;
#     END;
#     """
    
#     database_connection = None
#     cursor = None
#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute("DROP PROCEDURE IF EXISTS GetCustomerTourDetails")
#         cursor.execute(procedure_query)
#         database_connection.commit()
#     except Exception as e:
#         raise Exception(f"An error occurred while creating procedure: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection is not None:
#             database_connection.close()


# print(create_get_customer_tour_details_procedure())





# def total_customers():
#     cursor = None
#     database_connection = None
#     query = "SELECT COUNT(*) FROM contacts"
#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query)
#         result = cursor.fetchone()
#         return result[0]  # Getting the first element of the tuple
#     except Exception as e:
#         raise Exception(f"An error occurred while counting: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()





# def get_customers_information(page=1, items_per_page=25, search_query=''):
#     offset = (page - 1) * items_per_page
#     database_connection = None
#     contacts = []
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.callproc('GetCustomerTourDetails', [search_query, items_per_page, offset])
#         for result in cursor.stored_results():
#             contacts.extend(result.fetchall())
#     except Exception as e:
#         raise Exception(f"An error occurred while fetching customer information: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()

#     if len(contacts)==0:

#         return False

#     else:

#         return contacts





# def create_tour_bookings(tour_id, contact_id):
#     query = "INSERT INTO tour_bookings(tour_id, contact_id) VALUES(%s, %s)"
#     database_connection = None
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, (tour_id, contact_id))
#         database_connection.commit()
#         return True
#     except Exception as e:
#         logging.error(f"Error in create_tour_bookings: {e}")
#         if database_connection:
#             database_connection.rollback()
#         return False
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()




# def get_tour_id(tour_name, year):
#     query = "SELECT tour_id FROM tours WHERE TRIM(tour_name) = %s and YEAR(start_date) = %s"

#     database_connection = None
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, (tour_name,year))
#         result = cursor.fetchone()
#         return result[0] if result else None
#     except mysql.connector.Error as e:
#         # Handle specific database errors here
#         logging.error(f"Database error in get_tour_id: {e}")
#         return None
#     except Exception as e:
#         # Handle general errors here
#         logging.error(f"Error in get_tour_id: {e}")
#         return None
#     finally:
#         if database_connection:
#             database_connection.close()






# def get_customer_id(email):
#     query = "SELECT contact_id FROM contacts WHERE email_address = %s"
#     database_connection = None
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, (email,))
#         result = cursor.fetchone()
#         return result[0] if result else None
#     except Exception as e:
#         logging.error(f"Error in get_customer_id: {e}")
#         return None
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()





# def available_tour_dates():
#     current_year = datetime.date.today().year
#     query = """
#     SELECT Concat(tour_name, " ", YEAR(t.start_date))
#     FROM tours t
#     WHERE YEAR(t.start_date) >= %s
#     ORDER BY ABS(YEAR(start_date) - YEAR(CURDATE())) ASC, start_date DESC;"""
#     database_connection = None
#     cursor = None
#     dates = []

#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query,(current_year,))
#         date_tuples = cursor.fetchall()
#         dates = [date[0] for date in date_tuples]
#         return dates
#     except Exception as e:
#         logging.error(f"Error in available_tour_dates: {e}")
#         return []
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()





# def create_new_tourDates(tour_name, start_date, end_date, price, destination_id, tour_type):
#     query = "INSERT INTO tours(tour_name, start_date, end_date, tour_price, destination_id, tour_type) VALUES(%s, %s, %s, %s, %s, %s)"
#     database_connection = None
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, (tour_name, start_date, end_date, price, destination_id, tour_type))
#         database_connection.commit()
#         return True
#     except mysql.connector.Error as e:
#         logging.error(f"Database error in create_new_tourDates: {e}")
#         if database_connection:
#             database_connection.rollback()
#         return False
#     except Exception as e:
#         logging.error(f"Error in create_new_tourDates: {e}")
#         if database_connection:
#             database_connection.rollback()
#         return False
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()





# def add_new_paidCustomer(first_name, last_name, email, phone, gender ,state=None):
#     query = """
#         INSERT INTO contacts
#         (first_name, last_name, state_address, email_address, phone_number, gender)
#         VALUES (%s, %s, %s, %s, %s, %s)
#     """
#     values = (first_name, last_name, state, email, phone, gender)

#     try:
#         database_connection = create_databaseConnection()
#         if database_connection is not None:
#             cursor = database_connection.cursor()
#             cursor.execute(query, values)
#             database_connection.commit()
#             print("Customer successfully added with ID:", cursor.lastrowid)
#     except Error as e:
#         print(f"Database error occurred: {e}")
#         if database_connection:
#             database_connection.rollback()
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()






# def get_all_destination():
#     query = "SELECT destination_name FROM destinations"
#     destinations = []
#     database_connection = None
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         if database_connection:
#             cursor = database_connection.cursor()
#             cursor.execute(query)
#             destination_tuples = cursor.fetchall()
#             destinations = [destination[0] for destination in destination_tuples]
#         else:
#             logging.error("Failed to connect to the database")

#     except Exception as e:
#         destinations = []

#     finally:

#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()

#     return destinations






# def get_destination_id(destination_name):
#     destination= destination_name.capitalize()
#     query = "SELECT destination_id FROM destinations WHERE destination_name = %s"
#     database_connection = create_databaseConnection()
#     cursor = database_connection.cursor()
#     cursor.execute(query, (destination,))
#     result = cursor.fetchone()
#     cursor.close()
#     database_connection.close()
#     if result:
#         return result[0]
#     else:
#         return None




# def create_new_tourDates(tour_name, start_date, end_date, price, destination_id, tour_type):
#     query = "INSERT INTO tours(tour_name, start_date, end_date, tour_price, destination_id, tour_type) VALUES(%s, %s, %s, %s, %s, %s)"
#     values = (tour_name, start_date, end_date, price, destination_id, tour_type)

#     database_connection = None
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         if database_connection:
#             cursor = database_connection.cursor()
#             cursor.execute(query, values)
#             database_connection.commit()
#             return True
#         else:
#             logging.error("Failed to connect to the database")
#             return False

#     except mysql.connector.Error as db_err:
#         logging.error(f"Database error occurred: {db_err}")
#         return False

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         return False

#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()

#     return True






# def check_customer_exists(email):
#     query = "SELECT contact_id FROM contacts WHERE TRIM(LOWER(email_address)) = TRIM(LOWER(%s))"
#     contact_id = None

#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()

#         cursor.execute(query, (email,))
#         results = cursor.fetchall()  # Fetch all results to ensure all are consumed

#         # Log the number of entries found for the given email for debugging purposes.
#         if len(results) > 1:
#             logging.warning(f"Multiple entries found for {email}: {len(results)} entries.")

#         # Assuming the first row and first column is customer_id if any results are returned.
#         if results:
#             contact_id = results[0][0]

#     except mysql.connector.Error as db_err:
#         logging.error(f"Database error occurred: {db_err}")
#     except Exception as e:
#         logging.error(f"Error occurred: {e}")
#     finally:
#         if 'cursor' in locals() and cursor is not None:
#             try:
#                 cursor.close()
#             except mysql.connector.Error as err:
#                 logging.error(f"Error closing cursor: {err}")
#         if 'database_connection' in locals() and database_connection is not None:
#             try:
#                 database_connection.close()
#             except mysql.connector.Error as err:
#                 logging.error(f"Error closing connection: {err}")

#     return contact_id








# def get_total_numberOfTravellers():
#     target_year = datetime.datetime.now().year
#     query = """
#         SELECT COUNT(tb.booking_id)
#         FROM tour_bookings tb
#         JOIN tours t ON tb.tour_id = t.tour_id
#         WHERE YEAR(t.start_date) = %s
#     """
#     database_connection = None
#     cursor = None

#     try:
#         database_connection = create_databaseConnection()
#         if database_connection:
#             cursor = database_connection.cursor()
#             cursor.execute(query, (target_year,))
#             result = cursor.fetchone()
#             if result:
#                 return result[0]
#             else:
#                 return 0
#     except mysql.connector.Error as db_err:
#         logging.error(f"Database error occurred: {db_err}")
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()

#     return None




# def calculate_gross_revenue(year):
#     query = """
#         SELECT COALESCE(SUM(t.tour_price), 0) AS total_revenue
#         FROM tour_bookings tb
#         JOIN tours t ON tb.tour_id = t.tour_id
#         WHERE YEAR(t.start_date) = %s
#     """
#     try:
#         database_connection = create_databaseConnection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, (year,))  # Pass the year as a parameter to the query
#         result = cursor.fetchone()
#         total_revenue = result[0] if result else 0
#         revenue= float(total_revenue)
#         upper= int(revenue/1000)
#         middle= int(revenue-upper*1000)
#         lower=int(revenue*100-upper*100000-middle*100)
#         if upper==0:
#             format_rev= f"{middle}.{lower}"
    
#         else:
#             format_rev= f"{upper},{middle}.{lower}"
        
#         return format_rev,revenue


#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()





# def remove_paid_customer(contact_id):
#     deleted = False
#     database_connection = None
#     try:
#         database_connection = create_databaseConnection()
#         database_connection.autocommit = False
#         cursor = database_connection.cursor()
#         # cursor.execute("DELETE FROM tour_bookings WHERE customer_id=%s", (customer_id,))
#         # bookings_deleted = cursor.rowcount > 0
#         cursor.execute("DELETE FROM contacts WHERE contact_id=%s", (contact_id,))
#         customer_deleted = cursor.rowcount > 0
#         if customer_deleted:
#             database_connection.commit()
#             deleted = True
#         else:
#             database_connection.rollback()
#         cursor.close()
#     except Exception as e:
#         logging.error(f"An error occurred while deleting customer: {e}")
#         if database_connection:
#             database_connection.rollback()
#     finally:
#         if cursor:
#             cursor.close()
#         if database_connection:
#             database_connection.close()
#     return deleted






# bookings_deleted and

def create_database_connection():
    database_url = os.getenv('JAWSDB_URL')
    if database_url:
        parsed_url = urlparse(database_url)
        db_user = parsed_url.username
        db_password = parsed_url.password
        db_host = parsed_url.hostname
        db_name = parsed_url.path.lstrip('/')
        db_port = parsed_url.port
        try:
            sql_connection= mysql.connector.connect(
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

    procedure_query = """
        CREATE PROCEDURE GetCustomerTourDetails(
        IN search_query VARCHAR(255),
        IN items_per_page INT,
        IN offset INT)
    BEGIN
        IF search_query IS NULL OR search_query = '' THEN
            -- Original query without filtering, modified to include DISTINCT
            SELECT DISTINCT
                c.contact_id,
                CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                c.state_address AS `State`,
                c.email_address AS `Email`,
                c.phone_number AS `Mobile`,
                c.lead_status AS  `Lead Status`

            FROM
                contacts c
            JOIN
                tour_bookings tb ON tb.contact_id = c.contact_id
            JOIN
                tours t ON tb.tour_id = t.tour_id
            ORDER BY
                YEAR(t.start_date) DESC, c.contact_id DESC
            LIMIT items_per_page OFFSET offset;
        ELSE
            -- Query with filtering based on search_query, modified to include DISTINCT
            SELECT DISTINCT
                c.contact_id,
                CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                c.state_address AS `State`,
                c.email_address AS `Email`,
                c.phone_number AS `Mobile`,
                c.lead_status AS  `Lead Status`

            FROM
                contacts c
            JOIN
                tour_bookings tb ON tb.contact_id = c.contact_id
            JOIN
                tours t ON tb.tour_id = t.tour_id
            WHERE
                c.first_name LIKE CONCAT(search_query, '%') OR
                CONCAT(c.first_name, ' ', c.last_name) LIKE CONCAT('%', search_query, '%')
            ORDER BY
                YEAR(t.start_date) DESC, c.contact_id DESC
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
    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()






def total_customers():
    cursor = None
    database_connection = None
    query = "SELECT COUNT(*) FROM contacts"
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]  # Getting the first element of the tuple
    except Exception as e:
        raise Exception(f"An error occurred while counting: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def get_customers_information(page=1, items_per_page=25, search_query=''):
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

    if len(contacts)==0:

        return False

    else:

        return contacts




def create_tour_bookings(tour_id, contact_id):
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
        logging.error(f"Error in create_tour_bookings: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def get_tour_id(tour_name, year):
    query = "SELECT tour_id FROM tours WHERE TRIM(tour_name) = %s and YEAR(start_date) = %s"

    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (tour_name,year))
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as e:
        # Handle specific database errors here
        logging.error(f"Database error in get_tour_id: {e}")
        return None
    except Exception as e:
        # Handle general errors here
        logging.error(f"Error in get_tour_id: {e}")
        return None
    finally:
        if database_connection:
            database_connection.close()



def get_customer_id(email):
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



def available_tour_dates():
    current_year = datetime.date.today().year
    query = """
    SELECT Concat(tour_name, " ", YEAR(t.start_date))
    FROM tours t
    WHERE YEAR(t.start_date) >= %s
    ORDER BY ABS(YEAR(start_date) - YEAR(CURDATE())) ASC, start_date DESC;"""
    database_connection = None
    cursor = None
    dates = []

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query,(current_year,))
        date_tuples = cursor.fetchall()
        dates = [date[0] for date in date_tuples]
        return dates
    except Exception as e:
        logging.error(f"Error in available_tour_dates: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()



def create_new_tour_dates(tour_name, start_date, end_date, price, destination_id, tour_type):
    query = "INSERT INTO tours(tour_name, start_date, end_date, tour_price, destination_id, tour_type) VALUES(%s, %s, %s, %s, %s, %s)"
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (tour_name, start_date, end_date, price, destination_id, tour_type))
        database_connection.commit()
        return True
    except mysql.connector.Error as e:
        logging.error(f"Database error in create_new_tour_dates: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    except Exception as e:
        logging.error(f"Error in create_new_tour_dates: {e}")
        if database_connection:
            database_connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()



def add_new_paid_customer(first_name, last_name, email, phone, gender, state=None):
    query = """
        INSERT INTO contacts
        (first_name, last_name, state_address, email_address, phone_number, gender)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, state, email, phone, gender)

    try:
        database_connection = create_database_connection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            print("Customer successfully added with ID:", cursor.lastrowid)
    except Error as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()



def get_all_destinations():
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
    destination= destination_name.capitalize()
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




def check_customer_exists(email):
    query = "SELECT contact_id FROM contacts WHERE TRIM(LOWER(email_address)) = TRIM(LOWER(%s))"
    contact_id = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()

        cursor.execute(query, (email,))
        results = cursor.fetchall()  # Fetch all results to ensure all are consumed

        # Log the number of entries found for the given email for debugging purposes.
        if len(results) > 1:
            logging.warning(f"Multiple entries found for {email}: {len(results)} entries.")

        # Assuming the first row and first column is customer_id if any results are returned.
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
    query = """
        SELECT COALESCE(SUM(t.tour_price), 0) AS total_revenue
        FROM tour_bookings tb
        JOIN tours t ON tb.tour_id = t.tour_id
        WHERE YEAR(t.start_date) = %s
    """
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (year,))  # Pass the year as a parameter to the query
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





def remove_paid_customer(contact_id):
    deleted = False
    database_connection = None
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
