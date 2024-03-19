from  .models import create_database_connection
import sys 












def customers_location_by_state():
    query = """
        SELECT 
        CASE 
            WHEN state_address IS NULL THEN 'Unknown'
            WHEN state_address NOT IN (
                'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
                'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 
                'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 
                'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 
                'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC') THEN 'Other'
            ELSE state_address
        END AS state_group, 
        COUNT(*) AS customer_count
        FROM  contacts        #customers
        GROUP BY state_group
        ORDER BY customer_count DESC;
    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch all the rows in a list of lists.
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()


# data=customers_location_by_state()
# state_group=[]
# counts= []
# for states,count in data:
# 	state_group.append(states)
# 	counts.append(count)

# print(state_group)
# print(counts)



def customers_by_gender(year=None):
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
            GROUP BY gender_group;
        """
        params = {}

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, params)  # Use params to safely pass the year
        result = cursor.fetchall()  # Fetch all the rows in a list of lists.
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if database_connection is not None:
            database_connection.close()





def get_travellers_by_destination_query(year=None):
    # SQL query to count the number of bookings grouped by destination names
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
    
    # If a year is provided, add a WHERE clause to filter the results by that year
    if year is not None:
        query_parts.append(f"WHERE YEAR(t.start_date) = {year}")

    # Add GROUP BY and ORDER BY clauses to the query
    query_parts.extend([
        """
        GROUP BY
            d.destination_name
        ORDER BY
            Number_of_Bookings DESC;
        """
    ])

    # Combine all parts of the query into one full string
    query = " ".join(query_parts)
    
    # Execute the query against your database
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()  # replace with your actual connection function
        cursor = database_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()  # Fetch the results of the query
        return results  # Return the results to the caller
    except Exception as e:
        raise Exception(f"An error occurred while executing the query: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()









def calculate_annual_gross_revenue(year=None):
    # Base query to calculate total revenue
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
    
    # If a year is provided, add a WHERE clause to filter by that year
    if year is not None:
        query_parts.append("WHERE YEAR(t.start_date) = %s")
    
    # Add GROUP BY clause, grouping by year unless a specific year is given
    query_parts.append("GROUP BY revenue_year")

    # Combine all parts of the query into one full string
    query = " ".join(query_parts)
    
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        
        # Execute the query with or without the year parameter
        if year is not None:
            cursor.execute(query, (year,))
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        formatted_results = []

        # Format each year's revenue
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







   
