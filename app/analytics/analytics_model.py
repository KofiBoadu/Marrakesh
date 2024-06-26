from app.utils.database import create_database_connection
import datetime
import mysql.connector
import logging


def calculate_annual_gross_revenue(year=None):
    """
        Calculates the annual gross revenue from tour bookings, optionally filtered by a specific year.

        This function aggregates the total revenue from all tour bookings, grouping the results by year. If a specific year is provided, it calculates the total revenue for that year only.

        Parameters:
        - year (int, optional): The year for which to calculate gross revenue. If None, gross revenue for all years is calculated and grouped by year.

        Returns:
        - A list of tuples, where each tuple contains the year and the corresponding total revenue formatted as a string with two decimal places, or None if an error occurs.

        Note:
        - The function handles exceptions by printing an error message and returns None in such cases. The database connection is always closed before the function exits.
    """
    database_connection = None
    cursor = None
    query_parts = [
        """
        SELECT
            YEAR(t.start_date) AS revenue_year,
            COALESCE(SUM(t.tour_price), 0) AS total_revenue
        FROM
            tour_bookings tb
        JOIN
            tours t ON tb.tour_id = t.tour_id
        """
    ]

    if year is not None:
        query_parts.append("WHERE YEAR(t.start_date) = %s")

    query_parts.append("GROUP BY revenue_year")

    query = " ".join(query_parts)

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()

        if year is not None:
            cursor.execute(query, (year,))
        else:
            cursor.execute(query)

        results = cursor.fetchall()
        formatted_results = []

        for result in results:
            revenue_year, total_revenue = result
            revenue = float(total_revenue)
            formatted_revenue = f"{revenue:,.2f}"
            formatted_results.append((revenue_year, formatted_revenue))

        return formatted_results

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def get_travellers_by_destination_query(year=None):
    """
        Counts the number of bookings for each destination, optionally filtered by year.

        This function aggregates the total number of bookings for each destination. If a year is specified, it filters the bookings to only those starting within the given year.

        Parameters:
        - year (int, optional): The year to filter bookings by their start date. If None, bookings for all years are counted.

        Returns:
        - A list of tuples, each containing a destination name and the number of bookings for that destination, ordered by the number of bookings in descending order.

        Raises:
        - Exception: If an error occurs during query execution, an exception is raised with details of the error.

        Note:
        - The database connection is always properly closed before the function exits, regardless of whether an error occurred.
    """

    query_parts = [
        """
        SELECT
            d.destination_name,
            COUNT(tb.booking_id) AS Number_of_Bookings
        FROM
            destinations d
        JOIN
            tours t ON d.destination_id = t.destination_id
        JOIN
            tour_bookings tb ON t.tour_id = tb.tour_id
        """
    ]

    if year is not None:
        query_parts.append(f"WHERE YEAR(t.start_date) = {year}")
    query_parts.extend([
        """
        GROUP BY
            d.destination_name
        ORDER BY
            Number_of_Bookings DESC;
        """
    ])

    query = " ".join(query_parts)

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()  # replace with your actual connection function
        cursor = database_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        raise Exception(f"An error occurred while executing the query: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


# def contacts_by_gender(year=None):
#     """
#         Retrieves a count of contacts grouped by gender, optionally filtered by year.
#
#         This function can operate in two modes: if a year is provided, it returns the count of contacts by gender for tours starting or ending in that year; otherwise, it returns the count of all contacts by gender.
#
#         Parameters:
#         - year (int, optional): The year to filter the tour start and end dates. Defaults to None, in which case no year filter is applied.
#
#         Returns:
#         - A list of tuples, where each tuple contains a gender group ('male', 'female', or 'Other') and the count of contacts in that group.
#
#         Note:
#         - Handles database exceptions by printing an error message. The function ensures the database connection is closed before exiting.
#     """
#
#     if year:
#         query = """
#             SELECT
#                 CASE
#                     WHEN c.gender IN ('male', 'female') THEN c.gender
#                     ELSE 'Other'
#                 END AS gender_group,
#                 COUNT(*) as count
#             FROM contacts c
#             JOIN tour_bookings tb ON c.contact_id = tb.contact_id
#             JOIN tours t ON tb.tour_id = t.tour_id
#             WHERE (YEAR(t.start_date) = %(year)s OR YEAR(t.end_date) = %(year)s)
#             GROUP BY gender_group;
#         """
#         params = {'year': year}
#     else:
#         query = """
#             SELECT
#                 CASE
#                     WHEN gender IN ('male', 'female') THEN gender
#                     ELSE 'Other'
#                 END AS gender_group,
#                 COUNT(*) as count
#             FROM contacts
#             GROUP BY gender_group;
#         """
#         params = {}
#
#     database_connection = None
#     cursor = None
#     try:
#         database_connection = create_database_connection()
#         cursor = database_connection.cursor()
#         cursor.execute(query, params)
#         result = cursor.fetchall()
#         return result
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if database_connection is not None:
#             database_connection.close()

def customers_by_gender(year=None):
    """
    Retrieves a count of contacts grouped by gender, optionally filtered by year.

    Parameters:
    - year (int, optional): The year to filter the tour start and end dates. Defaults to None.

    Returns:
    - A list of tuples with each tuple containing a gender group and the count of contacts in that group.
    """

    # Build the query based on the presence of a year filter
    if year:
        query = """
            SELECT 
                CASE 
                    WHEN c.gender IN ('male', 'female') THEN c.gender
                    ELSE 'Other' 
                END AS gender_group,
                COUNT(*) as count
            FROM contacts c
            JOIN tour_bookings tb ON c.contact_id = tb.contact_id
            JOIN tours t ON tb.tour_id = t.tour_id
            WHERE (YEAR(t.start_date) = %(year)s OR YEAR(t.end_date) = %(year)s)
              AND c.lead_status = 'customer'
            GROUP BY gender_group;
        """
        params = {'year': year}
    else:
        query = """
            SELECT 
                CASE 
                    WHEN gender IN ('male', 'female') THEN gender
                    ELSE 'Other' 
                END AS gender_group,
                COUNT(*) as count
            FROM contacts
            WHERE lead_status = 'customer'
            GROUP BY gender_group;
        """
        params = {}

    database_connection = None
    cursor = None

    try:
        # Establish a connection to the database
        database_connection = create_database_connection()
        cursor = database_connection.cursor()

        # Execute the query and fetch results
        cursor.execute(query, params)
        results = cursor.fetchall()

        # Return the results
        return results
    except Exception as e:
        # Print the error message for debugging
        print(f"An error occurred while fetching gender data: {e}")
        return []
    finally:
        # Ensure both the cursor and connection are closed to release resources
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def customers_location_by_state():
    """
        Retrieves a count of customers grouped by their state address.

        This function queries the database to count how many customers are from each state or territory, including handling unknown or non-standard state addresses by grouping them under 'Unknown' or 'Other'.

        Returns:
        - A list of tuples, where each tuple contains a state or territory name (or 'Unknown'/'Other') and the count of customers from that location, ordered by count in descending order.

        Note:
        - The function handles exceptions by printing an error message but does not interrupt execution flow. The database connection is always closed before the function exits.
    """

    query = """
        SELECT 
            CASE 
                WHEN c.state_address IS NULL THEN 'Unknown'
                WHEN c.state_address NOT IN (
                    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
                    'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 
                    'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 
                    'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 
                    'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC') THEN 'Other'
                ELSE c.state_address
            END AS state_group, 
            COUNT(*) AS customer_count
        FROM 
            contacts c
        INNER JOIN 
            tour_bookings tb ON tb.contact_id = c.contact_id
        GROUP BY 
            state_group
        ORDER BY 
            customer_count DESC;
    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


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
