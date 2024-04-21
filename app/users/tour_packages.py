from app.utils.database import create_database_connection



def get_all_tours_scheduled():
    database_connection= None
    cursor= None 
    query= """

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
        ORDER BY YEAR(start_date) DESC;
    """
    try:
        database_connection= create_database_connection()
        cursor= database_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None 
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


# print(get_all_tours_scheduled())



    
    







    