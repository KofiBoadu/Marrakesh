from .models import create_database_connection




def profile_details(contact_id):
    query = """
        SELECT
          CONCAT(c.first_name, ' ', c.last_name) AS full_name,
          c.email_address,
          c.phone_number,
          c.state_address,
          c.lead_status,
          c.gender,
          GROUP_CONCAT(CONCAT(t.tour_type, " ", t.tour_name, ' ', YEAR(t.start_date)) SEPARATOR ', ') AS tour_details,
          SUM(t.tour_price) AS total_tour_price
        FROM
          contacts c
        JOIN
          tour_bookings tb ON c.contact_id = tb.contact_id
        JOIN
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
        return results[0] if results else None
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
            {"booking_id": row[0], "tour_id": row[1], "customer_id": row[2], "tour_name": row[3]} 
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




