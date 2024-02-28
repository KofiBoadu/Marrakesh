
from . import email_customers
from app.emails import send_email,customer_email_interactions,delete_customer_email
from flask import request, redirect, url_for, flash
from flask_login import login_required,current_user


@email_customers.route('/send-email', methods=['POST'])
@login_required
def send_customer_email():
    to_email = request.form.get('to_email')
    from_email = request.form.get('from_email')
    subject = request.form.get('subject')
    body = request.form.get('body')
    customer_id= request.form.get('customer_id')
    status = "email not sent"
    user= f"{current_user.first_name} {current_user.last_name}"
    email_sent = send_email(subject, from_email, [to_email], body)
    if email_sent:
        status = "sent"

    # user= f"{current_user.first_name} {current_user.last_name}"
    # print(user)

    store_email_details = customer_email_interactions(customer_id, subject, body, status,user)

    return redirect(url_for('profiles.customer_profile', customer_id=customer_id))



@email_customers.route('/delete-email/<int:customer_id>/<int:email_id>',methods=['POST'])
@login_required
def delete_email(email_id,customer_id):
    delete_the_email=delete_customer_email(email_id)
    customer_id= customer_id
    return redirect(url_for('profiles.customer_profile', customer_id=customer_id))
