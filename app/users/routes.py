from . import users_bp
from flask import  render_template, request,redirect,url_for,flash,session
from werkzeug.security import check_password_hash
from flask_login import login_user,UserMixin,logout_user
from app.user  import get_user,User
from flask_login import login_required




@users_bp.route('/login',methods=["GET"])
def login():
    return render_template("login.html")



@users_bp.route('/user',methods=['POST'])
def login_user_route():
    email = request.form.get('email')
    password = request.form.get('password')
    user= get_user(email)

    old_password=check_password_hash(user[4],password)
    if user and old_password:
        user_object=User(user[0],user[1],user[2],user[3],user[4])
        login_user(user_object)
        session['username'] = user[1].capitalize()
        return redirect(url_for("customers.home_page"))
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

