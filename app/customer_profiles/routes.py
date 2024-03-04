from flask import  render_template, request,redirect,url_for,flash
from app.profile_models import profile_details
from . import customers_profile
from app.emails import all_emails_sent_to_customer,send_email
from flask_login import login_required, current_user
from app.extension import cache
from app.models import format_phone_number,available_tour_dates,get_tour_id
from app.customer_models import update_customer_name,update_customer_email,update_customer_phone,change_customer_bookings,get_customer_activities,updating_customer_state
from app.customer_notes import  save_customer_notes, get_customer_notes,delete_customer_notes
from app.profile_models import get_customer_bookings






@customers_profile.route('/<int:customer_id>', methods=['GET'])
@login_required
def customer_profile(customer_id):
    if not customer_id:
        return redirect(url_for("customers.home_page"))
    else:
        profile = profile_details(customer_id)
      
        tour_names = profile[6]

        phone_number = format_phone_number(profile[2])

        if not tour_names:
            return redirect(url_for("customers.home_page"))
        tour_list= tour_names.split(', ')
       
        login_user=current_user.email_address

        booking_info = get_customer_bookings(customer_id)

        available_dates = available_tour_dates()
        activities = get_customer_activities(customer_id)
        return render_template('profile.html',activities=activities,available_dates=available_dates,booking_info=booking_info,login_user=login_user,profile=profile,tour_list=tour_list,customer_id=customer_id,phone_number=phone_number)





@customers_profile.route('/update-customer-reservations', methods=['POST'])
@login_required
def change_bookings():
    customer_id=request.form.get('updatingbooking_customer_id')
    new_tour_type=request.form.get('updatetour_date')
    checkbox_checked = 'notify-customer' in request.form
    customer_details= profile_details(customer_id)
    customer_name=profile_details(customer_id)[0].split()[0].capitalize()
    customer_email= customer_details[1]
    tour_date= new_tour_type.split()
    tour_year= tour_date.pop()
    tour_name=" ".join(tour_date)
    old_tour_name=request.form.get("modify_from")
    update_message=f"""Dear {customer_name},

           We have successfully updated your trip from {old_tour_name} to {new_tour_type}

      Warm regards,
      Africa Travellers
    """ 
    subject="Tour update"
    if checkbox_checked:
        send_email(subject,[customer_email],update_message)
        
    new_tour_id= get_tour_id(tour_name,tour_year)
    booking_id=request.form.get('updatingbooking_booking_id')
    change_customer_bookings(booking_id, new_tour_id, customer_id)
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





@customers_profile.route('/update_customer_state', methods=['POST'])
@login_required
def update_state_of_customers():
    customer_id= request.form.get('customer_id')
    new_state=request.form.get('new_state')
    updating_customer_state(new_state,customer_id)
    return redirect(url_for("profiles.customer_profile",customer_id=customer_id))





@customers_profile.route('/notes', methods=['POST'])
@login_required
def customer_notes():
    customer_id=request.form.get('customer_id')
    customer_notes=request.form.get('notes')
    creator=current_user.first_name + " "+ current_user.last_name
    save_customer_notes(customer_id, customer_notes,creator)
    return redirect(url_for("profiles.customer_profile",customer_id=customer_id))






@customers_profile.route('/delete_notes', methods=['POST'])
@login_required
def deleting_customer_notes():
    notes_id= request.form.get('notes_id')
    customer_id=request.form.get('customer_id')
    delete_customer_notes(notes_id, customer_id)
    return redirect(url_for("profiles.customer_profile",customer_id=customer_id))


