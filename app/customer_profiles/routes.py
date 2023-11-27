from flask import  render_template, request,redirect,url_for,flash
from app.profile_models import profile_details
from . import customers_profile
from app.emails import all_emails_sent_to_customer
from flask_login import login_required





@customers_profile.route('/<int:customer_id>', methods=['GET'])
@login_required
def customer_profile(customer_id):
    if not customer_id:
        return redirect(url_for("customers.home_page"))
    else:
        profile= profile_details(customer_id)
        tour_names=profile[4]
        if not tour_names:
            return redirect(url_for("customers.home_page"))
        tour_list= tour_names.split(', ')
        emails= all_emails_sent_to_customer(customer_id)
        return render_template('profile.html', profile=profile, tour_list=tour_list,customer_id=customer_id,emails=emails)

