from app.models import create_database_connection


def save_contact_notes(contact_id, note_message, note_creator):
    """
        Inserts a new note into the database for a specified contact.

        This function saves a note message associated with a contact ID into the database. It records who created the note and timestamps the entry automatically.

        Parameters:
        - contact_id (int): The ID of the contact for whom the note is being saved.
        - note_message (str): The content of the note being saved.
        - note_creator (str): Identifier (such as a username or ID) of the person or system that created the note.

        Raises:
        - Exception: If an error occurs during the database operation, an exception is raised with details of the error.

        Note:
        - The function attempts to open a database connection, execute the insert operation, and commit the changes. If an error occurs, it raises an exception with the error message. The database connection is always closed before the function exits, regardless of whether an error occurred.
    """
    database_connection = None
    cursor = None
    query = "INSERT INTO notes (contact_id, note_message, note_creator) VALUES (%s, %s, %s)"
    values = (contact_id, note_message, note_creator)

    try:
        database_connection = create_database_connection()
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


def get_contacts_notes(contact_id):
    """
        Retrieves all notes from the database associated with a specified contact ID.

        This function queries the database for notes related to a given contact, ordered by the note creation date in descending order, ensuring the most recent notes are returned first.

        Parameters:
        - contact_id (int): The ID of the contact whose notes are to be retrieved.

        Returns:
        - list: A list of tuples, each representing a note associated with the contact. Each tuple contains the note's ID, message, creation date, and creator. Returns an empty list if no notes are found or an error occurs.

        Note:
        - In case of a database error, the function will print an error message but will return an empty list to ensure the calling code can continue execution without handling exceptions.
    """
    database_connection = None
    cursor = None
    query = ("SELECT notes_id, note_message, date_created, note_creator FROM notes WHERE contact_id = %s ORDER BY "
             "notes_id DESC")

    try:
        database_connection = create_database_connection()
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


def delete_contacts_notes(notes_id, contact_id):
    """
        Deletes a specific note for a contact from the database.

        This function removes a note identified by its ID and associated with a given contact ID. It ensures that only notes belonging to the specified contact can be deleted.

        Parameters:
        - notes_id (int): The ID of the note to be deleted.
        - contact_id (int): The ID of the contact associated with the note.

        Note:
        - If an error occurs during the deletion process, an error message is printed and any changes are rolled back. The function ensures that the database connection is properly closed before exiting.

        Raises:
        - Prints an error message if the deletion operation fails due to a database error. Includes rollback of the transaction to ensure database integrity.
    """
    database_connection = None
    cursor = None
    query = "DELETE FROM notes WHERE notes_id = %s AND contact_id = %s"
    try:
        database_connection = create_database_connection()
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
