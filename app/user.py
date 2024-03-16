import secrets
import string
from werkzeug.security import generate_password_hash
from .models  import create_databaseConnection
from app.extension import login_manager
from flask_login import login_user,UserMixin


class User(UserMixin):
    def __init__(self,user_id,first_name,last_name,email_address,pass_word,role_id=None):
        self.id = user_id
        self.first_name=first_name
        self.last_name= last_name
        self.email_address=email_address
        self.pass_word= pass_word
        self.role_id= role_id




def generate_secure_password(length=12):
    characters=string.ascii_letters + string.digits + string.punctuation
    secure_password=""
    for i in range(length):
       secure_password= secure_password+secrets.choice(characters)
    return secure_password



def add_new_user(first_name, last_name, email_address,pass_word):
    cursor= None
    database_connection= None
    query= "INSERT INTO users(first_name,last_name,email_address,pass_word) VALUES(%s,%s,%s,%s)"
    values= (first_name, last_name,email_address,pass_word)
    try:
        database_connection= create_databaseConnection()
        cursor= database_connection.cursor()
        cursor.execute(query,values)
        database_connection.commit()
        return True
    except Exception as e :
        if database_connection:
            database_connection.rollback()
            print(e)
            return False
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def create_user_account(first_name, last_name, email_address):
    current_default_password= generate_secure_password()
    hash_password= generate_password_hash(current_default_password)
    add_new_user(first_name, last_name, email_address,hash_password)
    if not add_new_user:
        return False
    return current_default_password





def get_user(email):
    cursor = None
    database_connection = None
    query = "SELECT user_id,first_name,last_name,email_address,pass_word,role_id FROM users WHERE email_address = %s"
    try:
        database_connection = create_databaseConnection()
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


# print(get_user("mrboadu3@gmail.com"))



@login_manager.user_loader
def load_user(user_id):
    cursor = None
    database_connection = None
    query = "SELECT *  FROM users WHERE user_id = %s"
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (user_id,))
        user_details = cursor.fetchone()
        if user_details:
            # Create a new User object and return it
            return User(user_details[0], user_details[1], user_details[2], user_details[3],user_details[4])
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the exception
        return None  # Return None or an appropriate value indicating failure
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()




def pass_word_checker(password):
    if (len(password) > 8 and len(password  ) < 12):
        lower_case= False
        upper_case= False
        number= False
        special_char= False

        for each_character in password  :
            if each_character.isdigit():
                number= True
            if each_character.islower():
                lower_case  = True
            if each_character.isupper():
                upper_case  = True
            if each_character.isalnum():
                special_char= True
        return lower_case   and upper_case  and number  and special_char
    return False






def password_change(user_id ,new_password):
    cursor = None
    database_connection = None
    hash_password= generate_password_hash(new_password)
    query = "UPDATE users SET pass_word = %s WHERE user_id = %s"
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query, (hash_password, user_id))
        database_connection.commit()

    except Exception as e:
        print(f"Error updating password: {e}")

    finally :
        if cursor :
            cursor.close()
        if database_connection:
            database_connection.close()






def get_all_users():
    query= """ SELECT user_id, first_name, last_name, email_address, role_id FROM users """
    cursor= None 
    database_connection= None 
    try:
        database_connection = create_databaseConnection()
        cursor = database_connection.cursor()
        cursor.execute(query)
        results= cursor.fetchall()
        return results

    except Exception as e:
        print(f"An error occurred: {e}")  # Log the exception
        return None  # Return None or an appropriate value indicating failure
    finally:
        if cursor:
            cursor.close()
        if database_connection:
            database_connection.close()






