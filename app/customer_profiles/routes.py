from flask import  render_template, request,redirect,url_for,flash
from app.profile_models import profile_details
from . import customers_profile
from app.emails import all_emails_sent_to_customer
from flask_login import login_required
from app.extension import cache
from app.models import format_phone_number
from app.customer_models import update_customer_name,update_customer_email,update_customer_phone



@customers_profile.route('/<int:customer_id>', methods=['GET'])
@login_required
def customer_profile(customer_id):
    if not customer_id:
        return redirect(url_for("customers.home_page"))
    else:
        profile= profile_details(customer_id)
        tour_names=profile[4]
        phone_number=format_phone_number(profile[2])
        if not tour_names:
            return redirect(url_for("customers.home_page"))
        tour_list= tour_names.split(', ')
        emails= all_emails_sent_to_customer(customer_id)
        return render_template('profile.html', profile=profile, tour_list=tour_list,customer_id=customer_id,emails=emails,phone_number=phone_number)


@customers_profile.route('/', methods=['POST'])
@login_required
def customer_name():
    customer_id= request.form.get('customer_id')
    first_name = request.form.get('updatefirst_name')
    last_name = request.form.get('updatelast_name')
    update_customer_name(first_name, last_name,customer_id)
    return redirect(url_for("profiles.customer_profile", customer_id=customer_id))



@customers_profile.route('/', methods=['POST'])
@login_required
def customer_email():
    customer_id= request.form.get('customer_id')
    email = request.form.get('update_email')
    update_customer_email(email,customer_id)
    return redirect(url_for("profiles.customer_profile", customer_id=customer_id))




@customers_profile.route('/', methods=['POST'])
@login_required
def customer_phone():
    customer_id= request.form.get('customer_id')
    phone = request.form.get('update_phone')
    update_customer_phone(customer_id,phone)
    return redirect(url_for("profiles.customer_profile", customer_id=customer_id))

