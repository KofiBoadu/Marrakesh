from app.utils.database import create_database_connection
import logging
import mysql.connector










def update_full_contact_details(contact_id, first_name, last_name, email, phone, gender, state):
    """
        Updates the full contact details for a specific contact ID in the database.

        Parameters:
        - contact_id (int): Unique identifier for the contact.
        - first_name (str): The contact's first name.
        - last_name (str): The contact's last name.
        - email (str): The contact's email address.
        - phone (str): The contact's phone number.
        - gender (str): The contact's gender.
        - state (str): The state address of the contact.

        No explicit return value. Prints a message indicating whether the update was successful or if no customer was found.
        """

    query = """
       UPDATE contacts
        SET first_name = %s,
            last_name = %s,
            state_address = %s,
            email_address = %s,
            phone_number = %s,
            gender = %s
        WHERE contact_id = %s
    """
    values = (first_name, last_name, state, email, phone, gender, contact_id)
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            if cursor.rowcount > 0:
                print("Customer details successfully updated for ID:", contact_id)
            else:
                print("No customer found with ID:", contact_id)
    except Exception as e:
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def remove_contacts(contact_ids):
    """
    Deletes multiple contacts from the database based on their IDs. This operation is 
    typically performed after their accounts have been settled or closed.

    Parameters:
    - contact_ids (list of int): The IDs of the contacts to remove.

    Returns:
    - int: The number of contacts successfully deleted. This can be used to provide feedback or log the operation's success.

    Note:
    - This operation is transactional and will be rolled back if any errors occur during execution.
    """
    deleted_count = 0  # Initialize the count of deleted contacts
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()  
        database_connection.autocommit = False  
        cursor = database_connection.cursor()

        # Prepare the SQL query with placeholders for the list of IDs
        format_strings = ','.join(['%s'] * len(contact_ids))
        cursor.execute(f"DELETE FROM contacts WHERE contact_id IN ({format_strings})", tuple(contact_ids))

        deleted_count = cursor.rowcount  
        if deleted_count > 0:
            database_connection.commit()  
        else:
            database_connection.rollback()  
    except Exception as e:
        logging.error(f"An error occurred while deleting contacts: {e}")
        if database_connection:
            database_connection.rollback()  
    finally:
        if cursor:
            cursor.close()  
        if database_connection:
            database_connection.close()  
    return deleted_count  






def check_contact_exists(email):
    """
        Checks if a contact already exists in the database based on their email address.

        Parameters:
        - email (str): The email address of the contact to check.

        Returns:
        - The ID of the contact if they exist, None otherwise.

        Note:
        - This function is useful for avoiding duplicate entries in the database.
    """
    query = "SELECT contact_id FROM contacts WHERE TRIM(LOWER(email_address)) = TRIM(LOWER(%s))"
    contact_id = None
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()

        cursor.execute(query, (email,))
        results = cursor.fetchall()

        if len(results) > 1:
            logging.warning(f"Multiple entries found for {email}: {len(results)} entries.")

        if results:
            contact_id = results[0][0]

    except mysql.connector.Error as db_err:
        logging.error(f"Database error occurred: {db_err}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            try:
                cursor.close()
            except mysql.connector.Error as err:
                logging.error(f"Error closing cursor: {err}")
        if 'database_connection' in locals() and database_connection is not None:
            try:
                database_connection.close()
            except mysql.connector.Error as err:
                logging.error(f"Error closing connection: {err}")

    return contact_id





def get_total_num_of_contacts(search_query=''):
    """
    Counts the number of contacts in the database filtered by a search query if provided.
    """
    cursor = None
    database_connection = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        if search_query:
            query = """
            SELECT COUNT(*) FROM contacts
            WHERE LOWER(CONCAT(first_name, ' ', last_name, ' ', email_address, ' ', phone_number)) LIKE LOWER(%s)
            """
            cursor.execute(query, [f'%{search_query}%'])
        else:
            query = "SELECT COUNT(*) FROM contacts"
            cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        raise Exception(f"An error occurred while counting: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def get_filtered_contacts_count(status=None, gender=None, state=None, tour_name=None):
    """ Counts filtered contacts based on provided criteria. """
    query_parts = []
    params = []

    if status:
        query_parts.append("lead_status = %s")  # Ensure this matches the column name in the database.
        params.append(status)
    if gender:
        query_parts.append("gender = %s")
        params.append(gender)
    if state:
        query_parts.append("state_address = %s")  # Ensure this matches your stored procedure and actual column names.
        params.append(state)
    if tour_name:
        query_parts.append("tour_name LIKE %s")  # Using LIKE for partial matches.
        params.append(f"%{tour_name}%")

    query = "SELECT COUNT(*) FROM contacts"
    if query_parts:
        query += " WHERE " + " AND ".join(query_parts)

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, tuple(params))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print("An error occurred:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def get_contact_id(email):
    """
        Retrieves the contact ID for a given email address.

        Parameters:
        - email (str): The email address of the contact.

        Returns:
        - The contact ID if found, None otherwise.
    """
    query = "SELECT contact_id FROM contacts WHERE email_address = %s"
    database_connection = None
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logging.error(f"Error in get_customer_id: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()









def create_get_customer_tour_details_procedure():
    """
        Creates a stored procedure in the database to fetch customer tour details.

        The procedure supports pagination and optional filtering based on a search query.

        Returns:
        - True if the procedure is successfully created, raises an Exception otherwise.
    """
    procedure_query= """
        CREATE PROCEDURE GetCustomerTourDetails(
            IN search_query VARCHAR(255),
            IN items_per_page INT,
            IN offset INT)
        BEGIN
            IF search_query IS NULL OR search_query = '' THEN
                SELECT DISTINCT
                    c.contact_id,
                    CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                    c.state_address AS `State`,
                    c.email_address AS `Email`,
                    c.phone_number AS `Mobile`,
                    c.lead_status AS `Lead Status`,
                    COALESCE(CONCAT(u.first_name, ' ', u.last_name), 'unassigned') AS `Owner_Name`
                FROM
                    contacts c
                LEFT JOIN users u ON c.owner = u.user_id
                ORDER BY
                    c.contact_id DESC
                LIMIT items_per_page OFFSET offset;
            ELSE
                SELECT DISTINCT
                    c.contact_id,
                    CONCAT(c.first_name, ' ', c.last_name) AS `Full_Name`,
                    c.state_address AS `State`,
                    c.email_address AS `Email`,
                    c.phone_number AS `Mobile`,
                    c.lead_status AS `Lead Status`,
                    COALESCE(CONCAT(u.first_name, ' ', u.last_name), 'unassigned') AS `Owner_Name`
                FROM
                    contacts c
                LEFT JOIN users u ON c.owner = u.user_id
                WHERE
                    c.first_name LIKE CONCAT('%', search_query, '%') OR
                    c.last_name LIKE CONCAT('%', search_query, '%') OR
                    CONCAT(c.first_name, ' ', c.last_name) LIKE CONCAT('%', search_query, '%') OR
                    c.phone_number LIKE CONCAT('%', search_query, '%') OR
                    c.email_address LIKE CONCAT('%', search_query, '%')
                ORDER BY
                    c.contact_id DESC
                LIMIT items_per_page OFFSET offset;
            END IF;
        END;

    """

    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS GetCustomerTourDetails")
        cursor.execute(procedure_query)
        database_connection.commit()
        return True
    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")

    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()





def get_all_contacts_information(page=1, items_per_page=25, search_query=''):
    """
        Fetches contact information from the database with optional pagination and search filtering.

        Parameters:
        - page (int, optional): The current page number for pagination.
        - items_per_page (int, optional): The number of items per page for pagination.
        - search_query (str, optional): A search query to filter results.

        Returns:
        - A list of contacts matching the criteria or False if no contacts found. Raises an Exception on error.
    """
    offset = (page - 1) * items_per_page
    database_connection = None
    contacts = []
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.callproc('GetCustomerTourDetails', [search_query, items_per_page, offset])
        for result in cursor.stored_results():
            contacts.extend(result.fetchall())
    except Exception as e:
        raise Exception(f"An error occurred while fetching customer information: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    if len(contacts) == 0:

        return []

    else:

        return contacts

# print(get_all_contacts_information())



def add_new_contact(first_name, last_name, email, phone=None, gender=None, state=None, lead_status="Lead"):
    """
        Adds a new contact to the database with specified attributes.

        Parameters:
        - first_name (str): The first name of the contact.
        - last_name (str): The last name of the contact.
        - email (str): The email address of the contact.
        - phone (str, optional): The phone number of the contact.
        - gender (str, optional): The gender of the contact.
        - state (str, optional): The state of the contact.
        - lead_status (str, optional): The lead status of the contact, defaults to "Lead".

        Returns:
        - The ID of the newly added contact if the operation was successful, None otherwise.

        Note:
        - The function commits the new contact information to the database and returns the unique ID assigned to the contact.
    """
    query = """
        INSERT INTO contacts
        (first_name, last_name, state_address, email_address, phone_number, gender, lead_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    database_connection = None
    cursor = None
    values = (first_name, last_name, state, email, phone, gender, lead_status)
    try:
        database_connection = create_database_connection()
        if database_connection is not None:
            cursor = database_connection.cursor()
            cursor.execute(query, values)
            database_connection.commit()
            print("Customer successfully added with ID:", cursor.lastrowid)
            return cursor.lastrowid  # Return the new contact's ID
    except Exception as e:  # Catch a more general exception
        print(f"Database error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()





def filter_contacts_procedure():
    procedure_query="""
                CREATE PROCEDURE GetFilteredContacts(
                IN p_status VARCHAR(50),
                IN p_gender VARCHAR(10),
                IN p_state VARCHAR(50),
                IN p_tour_name VARCHAR(255),
                IN items_per_page INT,
                IN offset INT
            )
            BEGIN
                SET @sql = CONCAT('
                    SELECT DISTINCT
                        c.contact_id,
                        CONCAT(c.first_name, " ", c.last_name) AS `Full_Name`,
                        c.state_address AS `State`,
                        c.email_address AS `Email`,
                        c.phone_number AS `Mobile`,
                        c.lead_status AS `Lead Status`,
                        COALESCE(CONCAT(u.first_name, " ", u.last_name), "unassigned") AS `Owner_Name`
                    FROM
                        contacts c
                    LEFT JOIN users u ON c.owner = u.user_id
                    LEFT JOIN tour_bookings tb ON c.contact_id = tb.contact_id
                    LEFT JOIN tours t ON tb.tour_id = t.tour_id
                    WHERE 1=1
                ');
            
                IF p_status IS NOT NULL AND p_status != '' THEN
                    SET @sql = CONCAT(@sql, ' AND c.lead_status = "', p_status, '"');
                END IF;
                IF p_gender IS NOT NULL AND p_gender != '' THEN
                    SET @sql = CONCAT(@sql, ' AND c.gender = "', p_gender, '"');
                END IF;
                IF p_state IS NOT NULL AND p_state != '' THEN
                    SET @sql = CONCAT(@sql, ' AND c.state_address = "', p_state, '"');
                END IF;
                IF p_tour_name IS NOT NULL AND p_tour_name != '' THEN
                    SET @sql = CONCAT(@sql, ' AND t.tour_name LIKE "%', p_tour_name, '%"');
                END IF;
            
                SET @sql = CONCAT(@sql, ' ORDER BY c.contact_id DESC LIMIT ', items_per_page, ' OFFSET ', offset);
            
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            END;
    """
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS GetFilteredContacts")
        cursor.execute(procedure_query)
        database_connection.commit()
        return True
    except Exception as e:
        raise Exception(f"An error occurred while creating procedure: {e}")

    finally:
        if cursor:
            cursor.close()
        if database_connection is not None:
            database_connection.close()

# print(filter_contacts_procedure())

def get_filtered_information(page=1, items_per_page=25, status=None, gender=None, state=None, tour_name=None):
    """
        Fetches contact information from the database with optional pagination and filtering.

        Parameters:
        - page (int, optional): The current page number for pagination.
        - items_per_page (int, optional): The number of items per page for pagination.
        - status (str, optional): Filter by contact status.
        - gender (str, optional): Filter by gender.
        - state (str, optional): Filter by state.
        - tour_name (str, optional): Filter by tour name.

        Returns:
        - A list of contacts matching the criteria or an empty list if no contacts found. Raises an Exception on error.
    """
    offset = (page - 1) * items_per_page
    database_connection = None
    contacts = []
    cursor = None

    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        # Prepare parameters list for the stored procedure
        params = [status, gender, state, tour_name, items_per_page, offset]
        cursor.callproc('GetFilteredContacts', params)
        for result in cursor.stored_results():
            contacts.extend(result.fetchall())
    except Exception as e:
        raise Exception(f"An error occurred while fetching contact information: {e}")
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()

    return contacts if contacts else []

# print(get_filtered_information(status='customer'))
# print(get_filtered_contacts_count(status='customer'))