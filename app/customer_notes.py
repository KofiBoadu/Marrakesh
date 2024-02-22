from app.models import create_databaseConnection
import datetime



def save_customer_notes(customer_id, note_message):
    database_connection = None
    cursor = None
    query = "INSERT INTO notes (customer_id, note_message) VALUES (%s, %s)"
    values = (customer_id, note_message)
    
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, values)
        database_connection.commit()

    except Exception as e:
        raise Exception(f"An error occurred while saving customer notes: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()





def get_customer_notes(customer_id):
    database_connection = None
    cursor = None
    query = "SELECT note_message, date_created FROM notes WHERE customer_id = %s ORDER BY notes_id DESC"
    results = None

    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (customer_id,))
        results = cursor.fetchall()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return results






# print(get_customer_notes(1))


