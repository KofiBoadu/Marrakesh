from .models import create_database_connection



known_fields = {
    'message',
    'how_many_travelers',
    'enter_full_names_and_emails__of_other_travelers_if_any',
    'what_type_of_tour',
    'referral_name_or_code_if_any',
    'how_did_you_hear_about_us',
    'city',
    'postal_/_zip_code',
    'country',
    'type_of_accommodation',
    'payment_options',
    'address',
    'what_is_the_best_way_to_contact_you',
    'if_phone_when_is_the_best_time_of_day_for_a_call_back',
    'is_there_anything_else_we_should_know',
    'deposit_amount',
    'date',
    'time',
    'page_url',
    'form_name',
     "Accommodation Type",
     "Budget (Budget Excluding Flights)",
    " Destination",
     "Message",
     "Time",
    " What Is The Best Way To Contact You?",
    'Are you prepared to secure your spot with a deposit within the next week?'

  }




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
            cursor.execute("SELECT CONCAT(first_name, ' ', last_name) AS full_name, email_address, phone_number, state_address, lead_status, gender FROM contacts WHERE contact_id = %s", (contact_id,))
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





def contact_submissions(contact_id):
    query="""

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



# print(contact_submissions(413))




