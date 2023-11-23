import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import logging
import datetime




load_dotenv()
db_host = os.getenv("DATABASE_HOST")
db_user = os.getenv("DATABASE_USER")
db_password = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")



def create_databaseConnection():
    try:
        sql_connection= mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return sql_connection

    except Error as e :
        raise Exception(f"An error occurred while fetching customer information: {e}")





def create_get_customer_tour_details_procedure():
    procedure_query = """
    CREATE PROCEDURE GetCustomerTourDetails(IN target_year INT)
    BEGIN
        SELECT
            CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
            c.state_address AS `State`,
            c.email_address AS `Email`,
            c.phone_number AS `Mobile`,
            t.tour_name AS `Tour`,
            YEAR(t.start_date) AS `Travel_Year_Start`,
            YEAR(t.end_date) AS `Travel_Year_End`,
            t.tour_price AS `Tour_Price`,
            t.tour_type AS `Tour_Type`,
            d.destination_name AS `Destination`
        FROM
            customers c
        JOIN
            tour_bookings tb ON tb.customer_id = c.customer_id
        JOIN
            tours t ON tb.tour_id = t.tour_id
        JOIN
            destinations d ON t.destination_id = d.destination_id
        WHERE
            YEAR(t.start_date) = target_year
        ORDER BY
            c.customer_id DESC;
    END
    """

    database_connection = None
    try:
        database_connection = create_databaseConnection()
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








def get_customers_information(year):
    database_connection = None
    customers = []

    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.callproc('GetCustomerTourDetails', [year])
        for result in cursor.stored_results():
            customers.extend(result.fetchall())

    except Exception as e:
        raise Exception(f"An error occurred while fetching customer information: {e}")

    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return customers




def create_tour_bookings(tour_id, customer_id):
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()

        query = "INSERT INTO tour_bookings(tour_id, customer_id) VALUES(%s, %s)"
        values = (tour_id, customer_id)
        cursor.execute(query, values)
        database_connection.commit()
        return True

    except Exception as e:
        raise Exception(f"An error occurred: {e}")

    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def get_tour_id(tour_name):
    query = "SELECT tour_id FROM tours WHERE tour_name = %s"
    database_connection = create_databaseConnection()
    cursor = database_connection.cursor()
    cursor.execute(query, (tour_name,))
    result = cursor.fetchone()
    cursor.close()
    database_connection.close()
    if result:

        return result[0]
    else:

        return None




def get_customer_id(email):
    query = "SELECT customer_id FROM customers WHERE email_address = %s"
    database_connection = create_databaseConnection()
    cursor = database_connection.cursor()
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    database_connection.close()
    if result:

        return result[0]
    else:

        return None





def available_tour_dates():
    dates = []
    database_connection = None
    cursor = None
    try:
        database_connection = create_databaseConnection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            query = "SELECT tour_name FROM tours"
            cursor.execute(query)
            date_tuples = cursor.fetchall()
            dates = [date[0] for date in date_tuples]
        else:
            print("Failed to connect to the database")
    except Exception as e:
        raise Exception(f"An error occurred while getting  tour dates: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()
    return dates




def create_new_tourDates(tour_name, start_date,end_date,price,destination_id, tour_type):
     query = "INSERT INTO tours(tour_name, start_date,end_date,tour_price,destination_id,tour_type) VALUES(%s,%s,%s,%s,%s,%s)"
     values = (tour_name, start_date,end_date,price,destination_id, tour_type)
     try:
        database_connection = create_databaseConnection()
        with database_connection.cursor() as cursor:
            cursor.execute(query, values)
            database_connection.commit()
            return True
     except Exception as e:
        raise Exception(f"An error occurred while creating new tour dates: {e}")
     finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def add_new_paidCustomer(first_name, last_name, email, phone, gender, state=None):
    query = """
        INSERT INTO customers
        (first_name, last_name, state_address, email_address, phone_number, gender)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (first_name, last_name, state, email, phone, gender)

    try:
        database_connection = create_databaseConnection()
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






def get_all_destination():
    query = "SELECT destination_name FROM destinations"
    destinations = []
    database_connection = None
    cursor = None

    try:
        database_connection = create_databaseConnection()
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
    database_connection = create_databaseConnection()
    cursor = database_connection.cursor()
    cursor.execute(query, (destination,))
    result = cursor.fetchone()
    cursor.close()
    database_connection.close()
    if result:
        return result[0]
    else:
        return None




def create_new_tourDates(tour_name, start_date, end_date, price, destination_id, tour_type):
    query = "INSERT INTO tours(tour_name, start_date, end_date, tour_price, destination_id, tour_type) VALUES(%s, %s, %s, %s, %s, %s)"
    values = (tour_name, start_date, end_date, price, destination_id, tour_type)

    database_connection = None
    cursor = None

    try:
        database_connection = create_databaseConnection()
        if database_connection:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            return True
        else:
            logging.error("Failed to connect to the database")
            return False

    except mysql.connector.Error as db_err:
        logging.error(f"Database error occurred: {db_err}")
        return False

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return True




def check_customer_exists(email):
    query = "SELECT customer_id FROM customers WHERE email_address = %s"
    database_connection = None
    cursor = None
    customer_id = None

    try:
        database_connection = create_databaseConnection()
        if database_connection:
            cursor = database_connection.cursor()
            cursor.execute(query, (email,))
            customer = cursor.fetchone()
            if customer:
                customer_id = customer[0]
    except mysql.connector.Error as db_err:
        logging.error(f"Database error occurred: {db_err}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return customer_id




def get_total_numberOfTravellers():
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
        database_connection = create_databaseConnection()
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
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (year,))  # Pass the year as a parameter to the query
        result = cursor.fetchone()
        total_revenue = result[0] if result else 0
        return float(total_revenue)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





# # # print(get_tour_id("Ghana August 15th-24th"))
# # # print(get_customer_id("r1y9m4nd7@cox.net"))

# print(calculate_gross_revenue(2023))

# # # create_get_customer_tour_details_procedure()

# # # print( get_customers_information(2023))
