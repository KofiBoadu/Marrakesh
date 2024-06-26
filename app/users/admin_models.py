import secrets
import string
from werkzeug.security import generate_password_hash
from app.utils.database import create_database_connection
from app.utils.main import login_manager
from flask_login import login_user, UserMixin


class User(UserMixin):
    def __init__(self, user_id, first_name, last_name, email_address, pass_word, role_id=None):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.pass_word = pass_word
        self.role_id = role_id


def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_password = ""
    for i in range(length):
        secure_password = secure_password + secrets.choice(characters)
    return secure_password


def add_new_user(first_name, last_name, email_address, pass_word, role_id):
    cursor = None
    database_connection = None
    query = "INSERT INTO users(first_name,last_name,email_address,pass_word,role_id) VALUES(%s,%s,%s,%s,%s)"
    values = (first_name, last_name, email_address, pass_word, role_id)
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, values)
        database_connection.commit()

        return True
    except Exception as e:
        if database_connection:
            database_connection.rollback()
            print(e)
            return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def create_user_account(first_name, last_name, email_address, pass_word, role_id):
    hash_password = generate_password_hash(pass_word)
    add_user = add_new_user(first_name, last_name, email_address, hash_password, role_id)
    if not add_user:
        return False
    return True


# password=generate_secure_password()
# print(password)
# add=create_user_account("Africa","Travellers","bookings@africatravellers.com",password,1)
# print(add)

def get_user(email):
    cursor = None
    database_connection = None
    query = ("SELECT user_id,first_name,last_name,email_address,pass_word,role_id, is_active FROM users WHERE "
             "email_address = %s")
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (email,))
        user_details = cursor.fetchone()
        return user_details
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


# print(get_user("bookings@africatravellers.com"))

@login_manager.user_loader
def load_user(user_id):
    cursor = None
    database_connection = None
    query = "SELECT *  FROM users WHERE user_id = %s"
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (user_id,))
        user_details = cursor.fetchone()
        if user_details:
            # Create a new User object and return it
            return User(user_details[0], user_details[1], user_details[2], user_details[3], user_details[4])
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the exception
        return None  # Return None or an appropriate value indicating failure
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def pass_word_checker(password):
    if 8 < len(password) < 12:
        lower_case = False
        upper_case = False
        number = False
        special_char = False

        for each_character in password:
            if each_character.isdigit():
                number = True
            if each_character.islower():
                lower_case = True
            if each_character.isupper():
                upper_case = True
            if each_character.isalnum():
                special_char = True
        return lower_case and upper_case and number and special_char
    return False


def password_change(user_id, new_password):
    cursor = None
    database_connection = None
    hash_password = generate_password_hash(new_password)
    query = "UPDATE users SET pass_word = %s WHERE user_id = %s"
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (hash_password, user_id))
        database_connection.commit()
        return True

    except Exception as e:
        print(f"Error updating password: {e}")

    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


#
# password=generate_secure_password()
# print("new password",password)
# add=password_change(1,password)
# print(add)

def get_all_users():
    query = """ 
    SELECT users.user_id, users.first_name, users.last_name, users.email_address, user_roles.role_name
    FROM users
    LEFT JOIN user_roles ON users.role_id = user_roles.role_id
    """
    cursor = None
    database_connection = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return [(user_id, first_name, last_name, email_address, role_name if role_name else 'No Role Assigned') for
                user_id, first_name, last_name, email_address, role_name in results]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


# print(get_all_users())


def remover_user_from_account(user_id):
    query = "DELETE FROM users WHERE user_id=%s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (user_id,))
        database_connection.commit()
        return True
    except Exception as e:
        print(f"OOps !!! this happened:  {e}")
        if database_connection:
            database_connection.rollback()

    finally:
        if database_connection:
            database_connection.close()
        if cursor:
            cursor.close()


def user_roles():
    query = "SELECT role_id, role_name FROM user_roles"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"an error occured: {e}")

    finally:
        if database_connection:
            database_connection.close()
        if cursor:
            cursor.close()


def deactivate_user_account(user_id):
    query = "UPDATE users SET is_active = 0 WHERE user_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()  #
        cursor = database_connection.cursor()  # Fixed from .close() to .cursor()
        cursor.execute(query, (user_id,))
        database_connection.commit()

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def reactivate_user_account(user_id):
    query = "UPDATE users SET is_active = 1 WHERE user_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()  #
        cursor = database_connection.cursor()  # Fixed from .close() to .cursor()
        cursor.execute(query, (user_id,))
        database_connection.commit()

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def remove_super_admin(user_id):
    query = "UPDATE users SET role_id = 2 WHERE user_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()  #
        cursor = database_connection.cursor()  # Fixed from .close() to .cursor()
        cursor.execute(query, (user_id,))
        database_connection.commit()

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def make_super_admin(user_id):
    query = "UPDATE users SET role_id = 1 WHERE user_id = %s"
    database_connection = None
    cursor = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (user_id,))
        database_connection.commit()

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        if database_connection:
            database_connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def update_user_time_zone(user_id, time_zone):
    query = """UPDATE users SET timezone = %s WHERE user_id = %s"""
    cursor = None
    database_connection = None
    try:

        database_connection = create_database_connection()
        cursor = database_connection.cursor()

        cursor.execute(query, (time_zone, user_id))
        database_connection.commit()

        return True

    except Exception as e:

        if database_connection:
            database_connection.rollback()
        return False

    finally:

        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


def change_user_name_details(first_name, last_name, user_id):
    query = """UPDATE users SET first_name = %s, last_name = %s WHERE user_id = %s"""
    cursor = None
    database_connection = None
    try:
        database_connection = create_database_connection()
        cursor = database_connection.cursor()
        cursor.execute(query, (first_name, last_name, user_id))
        database_connection.commit()
        return True
    except Exception as e:
        if database_connection:
            database_connection.rollback()
        print("An error occurred updating user first name and last name:", e)
        return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()


