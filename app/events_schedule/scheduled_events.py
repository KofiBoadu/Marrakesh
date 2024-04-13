from app.utils.database import create_database_connection


def all_scheduled_events():
    database_connection = None
    cursor = None
    # Modified query to select all future tours, not filtering by tour_id
    query = """
    SELECT tour_name, start_date, end_date, tour_type
    FROM tours
    WHERE start_date >= CURDATE()
    ORDER BY start_date ASC
    """

    scheduled_events = []
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        # Organizing the response into a list of dictionaries
        scheduled_events = [{'tour_name': event[0], 'start_date': event[1], 'end_date': event[2], 'tour_type': event[3]}
                            for event in results]
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()
    return scheduled_events
