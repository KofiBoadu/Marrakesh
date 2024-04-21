from . import users_bp
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from .admin_models import get_user, User, create_user_account, generate_secure_password, deactivate_user_account, \
    reactivate_user_account, remove_super_admin, make_super_admin
from flask_login import login_required, current_user
from .admin_models import password_change, pass_word_checker, get_all_users, remover_user_from_account, user_roles
from app.utils.main import send_email
from app.utils.tours import get_all_destinations
from app.users.tour_packages import get_all_tours_scheduled







@users_bp.route('/login', methods=["GET"])
def login():
    return render_template("login.html")


@users_bp.route('/user', methods=['POST'])
def login_user_route():
    email = request.form.get('email')
    password = request.form.get('password')
    user = get_user(email)
    old_password = check_password_hash(user[4], password)
    if user and old_password and user[6]:
        old_password = check_password_hash(user[4], password)
        print("old password", old_password)
        user_object = User(user[0], user[1], user[2], user[3], user[4], user[5])
        login_user(user_object)
        user_id = user[0]
        first_name = user[1]
        last_name = user[2]
        session['username'] = [user_id, first_name, last_name]
        role_id = user[5]
        session['user_role_id'] = role_id
        return redirect(url_for("contacts.home_page"))
    else:
        return redirect(url_for('users.login'))


@users_bp.context_processor
def user():
    username = session.get('username')
    if username:
        return {'username': username}
    return {'username': None}



@users_bp.route('/logout')
@login_required
def log_out():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('users.login'))


@users_bp.route('/password-reset', methods=['GET', 'POST'])
@login_required
def password_reset():
    if request.method == "GET":
        return render_template('reset_password.html')

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        user = session.get('username')
        user_id = user[0]

        if not pass_word_checker(new_password):
            flash("Password does not meet requirements.")
            return redirect(url_for('users.password_reset'))

        elif new_password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('users.password_reset'))
        else:
            password_change(user_id, new_password)
            return redirect(url_for('customers.home_page'))  # Make sure 'customers_bp' is your Blueprint name






@users_bp.route('/settings/user/profile', methods=['GET'])
@login_required
def user_profile():
    user = current_user
    return render_template('general.html', user=user)







@users_bp.route('/settings/users/', methods=['GET', "POST"])
@login_required
def settings_users():
    users = get_all_users()
    available_roles = user_roles()
    return render_template('users_teams.html', users=users, available_roles=available_roles)








@users_bp.route('/settings/services/management/', methods=['GET', "POST"])
@login_required
def services():
    destinations= get_all_destinations()
    return render_template('service_management.html',destinations=destinations)






@users_bp.route('/remove_user', methods=["POST"])
@login_required
def remove_a_user():
    user_id = request.form.get('user_id')
    if user_id:
        remover_user_from_account(user_id)  
    return redirect(url_for('users.settings_users'))






@users_bp.route('/settings/user-created/', methods=["POST"])
@login_required
def creating_users():
    new_user_role_id = request.form.get("role_id")
    new_user_first_name = request.form.get('user_first_name')
    new_user_last_name = request.form.get('user_last_name')
    new_user_email = request.form.get('new-user-email')
    temp_password = generate_secure_password()
    subject = "Welcome to the Marrakesh team!"
    account_creation_success = create_user_account(new_user_first_name, new_user_last_name, new_user_email,
                                                   temp_password, new_user_role_id)

    if account_creation_success:
        invite_message = f"""Dear {new_user_first_name},

Thank you for joining the Marrakesh team. Below are your temporary credentials to access your account. You should be able to reset your password when you login with your temporary password.

Login email: {new_user_email}
Temporary password: {temp_password}
URL: https://africatravellers-crm-7ca32dc61ea0.herokuapp.com/contacts/contacts/home

Thank you,
Marrakesh Team
"""

        send_email(subject, [new_user_email], invite_message)
    return redirect(url_for('users.settings_users'))





@users_bp.route('/settings/deactivate/user', methods=["POST"])
@login_required
def deactivate_user():
    user_id = request.form.get('user_id')
    if user_id:
        deactivate_user_account(user_id)
    else:
        print("could not fine the user ID ")
    return redirect(url_for('users.settings_users'))





@users_bp.route('/settings/reactivate/user', methods=["POST"])
@login_required
def reactivate_user():
    user_id = request.form.get('user_id')
    if user_id:
        reactivate_user_account(user_id)
    else:
        print("could not fine the user ID ")
    return redirect(url_for('users.settings_users'))





@users_bp.route('/settings/remove-admin-role/', methods=["POST"])
@login_required
def remove_admin_role():
    user_id = request.form.get('user_id')
    if user_id:
        remove_super_admin(user_id)
    else:
        print("could not fine the user ID ")
    return redirect(url_for('users.settings_users'))





@users_bp.route('/settings/make-admin-role/', methods=["POST"])
@login_required
def make_admin_role():
    user_id = request.form.get('user_id')
    if user_id:
        make_super_admin(user_id)
    else:
        print("could not fine the user ID ")
    return redirect(url_for('users.settings_users'))






@users_bp.route('/settings/tour/packages', methods=["GET"])
def tour_services():
    tours_scheduled= get_all_tours_scheduled()
    destinations= get_all_destinations()
    tour_id= tours_scheduled[0][0]
    return render_template('service_management.html',tour_id=tour_id,tours_scheduled=tours_scheduled,destinations=destinations)
    