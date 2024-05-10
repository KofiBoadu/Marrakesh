from . import email_customers
from app.utils.main import send_email,contact_email_interactions,delete_contacts_email,update_contact_owner
from flask import request, redirect, url_for
from flask_login import login_required,current_user


@email_customers.route('/send-email', methods=['POST'])
@login_required
def send_contact_email():
    to_email = request.form.get('to_email')
    from_email = request.form.get('from_email')
    subject = request.form.get('subject')
    body = request.form.get('body')
    contact_id= request.form.get('contact_id')
    status = "email not sent"
    user= f"{current_user.first_name} {current_user.last_name}"
    user_id= current_user.id
    email_sent = send_email(subject, [to_email], body)
    if email_sent:
        status = "sent"
        contact_email_interactions(contact_id, subject, body, status, user)
        update_contact_owner(contact_id,user_id)

    return redirect(url_for('profiles.contact_profile', contact_id=contact_id))



@email_customers.route('/delete-email/<int:contact_id>/<int:email_id>',methods=['POST'])
@login_required
def delete_email(email_id,contact_id):
    delete_contacts_email(email_id)
    contact_id= contact_id
    return redirect(url_for('profiles.contact_profile', contact_id=contact_id))
