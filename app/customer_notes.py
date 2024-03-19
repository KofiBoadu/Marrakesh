from app.models import create_databaseConnection
import datetime



def save_customer_notes(contact_id, note_message,note_creator):
    database_connection = None
    cursor = None
    query = "INSERT INTO notes (contact_id, note_message,note_creator) VALUES (%s, %s,%s)"
    values = (contact_id, note_message,note_creator)
    
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





def get_customer_notes(contact_id):
    database_connection = None
    cursor = None
    query = "SELECT notes_id, note_message, date_created, note_creator FROM notes WHERE contact_id = %s ORDER BY notes_id DESC"
    results = []

    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (contact_id,))
        results = cursor.fetchall()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        results = []  # Ensure that results is always a list, even after an exception.
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return results



def delete_customer_notes(notes_id, contact_id):
    database_connection = None
    cursor = None
    query = "DELETE FROM notes WHERE notes_id = %s AND contact_id = %s"
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (notes_id, contact_id))
        database_connection.commit()
    except Exception as e:
        print(f"An error occurred while deleting the note: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


    







# print(get_customer_notes(1))


