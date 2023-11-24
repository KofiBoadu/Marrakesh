from flask import  render_template, request,redirect,url_for,flash
from app.profile_models import profile_details
from . import customers_profile






@customers_profile.route('/<int:customer_id>', methods=['GET'])
def customer_profile(customer_id):
    profile= profile_details(customer_id)
    tour_names=profile[4]
    tour_list= tour_names.split(', ')
    return render_template('profile.html', profile=profile, tour_list=tour_list)
