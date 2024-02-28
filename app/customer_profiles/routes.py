from flask import  render_template, request,redirect,url_for,flash
from app.profile_models import profile_details
from . import customers_profile
from app.emails import all_emails_sent_to_customer
from flask_login import login_required, current_user
from app.extension import cache
from app.models import format_phone_number,available_tour_dates,get_tour_id
from app.customer_models import update_customer_name,update_customer_email,update_customer_phone,change_customer_bookings
from app.customer_notes import  save_customer_notes, get_customer_notes,delete_customer_notes
from app.profile_models import get_customer_bookings


@customers_profile.route('/<int:customer_id>', methods=['GET'])
@login_required
def customer_profile(customer_id):
    if not customer_id:
        return redirect(url_for("customers.home_page"))
    else:
        profile= profile_details(customer_id)
        tour_names=profile[6]
        phone_number=format_phone_number(profile[2])
        if not tour_names:
            return redirect(url_for("customers.home_page"))
        tour_list= tour_names.split(', ')
        emails= all_emails_sent_to_customer(customer_id)

        notes= get_customer_notes(customer_id)
        login_user=current_user.email_address

        booking_info=get_customer_bookings(customer_id)

        available_dates= available_tour_dates()
        
        return render_template('profile.html',available_dates=available_dates,booking_info=booking_info,login_user=login_user,profile=profile,notes=notes,tour_list=tour_list,customer_id=customer_id,emails=emails,phone_number=phone_number)





@customers_profile.route('/update-customer-reservations', methods=['POST'])
def change_bookings():
    customer_id=request.form.get('updatingbooking_customer_id')
    new_tour_type=request.form.get('updatetour_date')
    tour_date= new_tour_type.split()
    tour_year= tour_date.pop()
    tour_name=" ".join(tour_date)
    new_tour_id= get_tour_id(tour_name,tour_year)
    booking_id=request.form.get('updatingbooking_booking_id')
    change_customer_bookings(booking_id, new_tour_id, customer_id)
    # print(tour_id)
    # print(tour_name)
    return redirect(url_for("profiles.customer_profile",customer_id=customer_id))








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









@customers_profile.route('/notes', methods=['POST'])
@login_required
def customer_notes():
    customer_id=request.form.get('customer_id')
    customer_notes=request.form.get('notes')
    save_customer_notes(customer_id, customer_notes)
    return redirect(url_for("profiles.customer_profile",customer_id=customer_id))









@customers_profile.route('/delete_notes', methods=['POST'])
@login_required
def deleting_customer_notes():
    notes_id= request.form.get('notes_id')
    customer_id=request.form.get('customer_id')
    delete_customer_notes(notes_id, customer_id)
    return redirect(url_for("profiles.customer_profile",customer_id=customer_id))

    



