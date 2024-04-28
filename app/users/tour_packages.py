from app.utils.database import create_database_connection





def get_all_tours_procedure():
    create_procedure_query = """
     CREATE PROCEDURE GET_TOUR_PACKAGES(
            IN _items_per_page INT,
            IN _page_number INT
        )
        BEGIN
            DECLARE _offset INT DEFAULT (_page_number - 1) * _items_per_page;

        SELECT
            tour_id,
            tour_name,
            start_date,
            end_date,
            tour_price,
            destination_name,
            tour_type

        FROM tours

        JOIN destinations ON destinations.destination_id = tours.destination_id
        ORDER BY YEAR(start_date) DESC
        LIMIT _items_per_page OFFSET _offset;

        END;
    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS GET_TOUR_PACKAGES")
        cursor.execute(create_procedure_query)
        database_connection.commit()
        print("Stored procedure created successfully.")
        return True
    except Exception as e:
        print(f"An error occurred while creating the procedure: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

# print(get_all_tours_procedure())


def get_all_tours_scheduled(page=1, items_per_page=10):
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.callproc('GET_TOUR_PACKAGES', [items_per_page,page])
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()



def get_total_tour_packages():
    # Correct SQL query to count rows in the TOURS table
    query = "SELECT COUNT(*) FROM TOURS"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        # Correct method to fetch the result
        results = cursor.fetchone()
        return results[0]  # Assuming you want to return the count directly
    except Exception as e:  # Removed unnecessary parentheses around 'e'
        print(f"An error occurred: {e}")
        return 0  # Returning 0 to indicate no tours found or error occurred
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


# print(get_total_tour_packages())



# print(len(get_all_tours_scheduled(2)))
    







    