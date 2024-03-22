from flask import  render_template, request,redirect,url_for,flash
from app.profile_models import profile_details
from . import customers_profile
from app.emails import all_emails_sent_to_customer,send_email
from flask_login import login_required, current_user
from app.extension import cache
from app.models import create_tour_bookings,format_phone_number,available_tour_dates,get_tour_id,all_states
from app.customer_models import updating_contact_status,update_customer_name,update_customer_email,update_contact_phone,change_customer_bookings,get_customer_activities,updating_contact_state,bookings_updates_logs,get_customer_booking_changes
from app.customer_notes import  save_customer_notes, get_customer_notes,delete_customer_notes
from app.profile_models import get_customer_bookings,contact_submissions,known_fields






@customers_profile.route('/<int:contact_id>', methods=['GET'])
@login_required
def customer_profile(contact_id):
    if not contact_id:
        return redirect(url_for("customers.home_page"))
    else:
        profile = profile_details(contact_id)
        if not profile:
            return redirect(url_for("customers.home_page"))

        tour_names = profile[6]
        tour_list = tour_names.split(', ') if tour_names else []

        phone_number = format_phone_number(profile[2]) if profile[2] else "Not Provided"

        booking_info = get_customer_bookings(contact_id) if tour_list else []

        available_dates = available_tour_dates()

        activities = get_customer_activities(contact_id)

        states = all_states()

        results=contact_submissions(contact_id)
        print(results)

        known_field=known_fields

        form_fields_dict = {field: '' for field in known_field}

        common_data={}

        if results:
            common_data = {
            'name': f"{results[0][0]} {results[0][1]}",
            'submission_source': results[0][2],
            'submission_date': results[0][3].strftime('%B %d, %Y %I:%M %p')
                }

            for _, _, _, _, field_name, field_value in results:
                if field_name in known_field:
                    field_display_name = field_name.replace('_', ' ').title()
                    form_fields_dict[field_display_name] = field_value

        # print("Common data",common_data)

        # form_fields = submission[4:]

        # print("form fields",form_fields)

        login_user = login_user=current_user.email_address
        return render_template('profile.html',common_data=common_data,form_fields=form_fields_dict,states=states, activities=activities, available_dates=available_dates, booking_info=booking_info, login_user=login_user, profile=profile, tour_list=tour_list, contact_id=contact_id, phone_number=phone_number)




@customers_profile.route('/update-customer-reservations', methods=['POST'])
@login_required
def change_bookings():
    contact_id=request.form.get('updatingbooking_contact_id')
    print("ID",contact_id)
    new_tour_type=request.form.get('updatetour_date')
    checkbox_checked = 'notify-customer' in request.form
    customer_details= profile_details(contact_id)

    customer_name=profile_details(contact_id)[0].split()[0].capitalize()
    customer_email= customer_details[1]
    tour_date= new_tour_type.split()
    tour_year= tour_date.pop()
    tour_name=" ".join(tour_date)


    old_tour_name=request.form.get("modify_from")
    old_tour_date= old_tour_name.split()
    old_tour_year=old_tour_date.pop()
    new_old_tour_name=" ".join(old_tour_date)

    update_message=f"""Dear {customer_name},

           We have successfully updated your trip from {old_tour_name} to {new_tour_type}

      Warm regards,
      Africa Travellers
    """

    subject="Tour update"
    if checkbox_checked:
        send_email(subject,[customer_email],update_message)

        
    new_tour_id= get_tour_id(tour_name,tour_year)
    old_tour_id= get_tour_id(new_old_tour_name,old_tour_year)


    user_id= current_user.id
    update_details_message= f" Tour was updated from {old_tour_name} to {new_tour_type}"


    bookings_updates_logs(old_tour_id, new_tour_id,contact_id, user_id, update_details_message)


    booking_id=request.form.get('updatingbooking_booking_id')
    change_customer_bookings(booking_id, new_tour_id, contact_id)
    return redirect(url_for("profiles.customer_profile",contact_id=contact_id))







@customers_profile.route('/change-contacts-name', methods=['POST'])
@login_required
def customer_name():
    contact_id= request.form.get('contact_id')
    first_name = request.form.get('updatefirst_name')
    last_name = request.form.get('updatelast_name')
    update_customer_name(first_name, last_name,contact_id)
    return redirect(url_for("profiles.customer_profile", contact_id=contact_id))








@customers_profile.route('/change-contacts-email', methods=['POST'])
@login_required
def customer_email():
    contact_id= request.form.get('contact_id')
    email = request.form.get('update_email')
    update_customer_email(email,contact_id)
    return redirect(url_for("profiles.customer_profile", contact_id=contact_id))






@customers_profile.route('/change-contact-phone', methods=['POST'])
@login_required
def update_contact_phone_number():
    contact_id= request.form.get('contact_id')
    print(contact_id)
    phone = request.form.get('update_phone')
    print(phone)
    update_contact_phone(contact_id,phone)
    return redirect(url_for("profiles.customer_profile", contact_id=contact_id))





@customers_profile.route('/update_customer_state', methods=['POST'])
@login_required
def update_state_of_contact():
    contact_id= request.form.get('contact_id')
    new_state=request.form.get('new_state')
    updating_contact_state(new_state,contact_id)
    return redirect(url_for("profiles.customer_profile",contact_id=contact_id))





@customers_profile.route('/notes', methods=['POST'])
@login_required
def customer_notes():
    contact_id=request.form.get('contact_id')
    customer_notes=request.form.get('notes')
    creator=current_user.first_name + " "+ current_user.last_name
    save_customer_notes(contact_id, customer_notes,creator)
    return redirect(url_for("profiles.customer_profile",contact_id=contact_id))






@customers_profile.route('/delete_notes', methods=['POST'])
@login_required
def deleting_customer_notes():
    notes_id= request.form.get('notes_id')
    contact_id=request.form.get('contact_id')
    delete_customer_notes(notes_id, contact_id)
    return redirect(url_for("profiles.customer_profile",contact_id=contact_id))





@customers_profile.route('/change-contact-status',methods=['POST'])
@login_required
def new_contact_status():
    contact_id=request.form.get('contact_id')
    new_status= request.form.get('new_contact_status_name')
    updating_contact_status(new_status,contact_id)
    return redirect(url_for("profiles.customer_profile",contact_id=contact_id))





@customers_profile.route('/making-tour-reservation',methods=['POST'])
@login_required
def confirm_contact_tour_bookings():
    contact_id=request.form.get('contact_id')
    selected_tour= request.form.get('tour_date')
    profile = profile_details(contact_id)
    if contact_id and selected_tour:
        tour_date=selected_tour.split()
        tour_year= tour_date.pop()
        tour_name=" ".join(tour_date)
        tour_id=get_tour_id(tour_name,tour_year)
        create_tour_bookings(tour_id,contact_id)
        if profile[4] != "customer":
            new_status="customer"
            updating_contact_status(new_status,contact_id)
        return redirect(url_for("profiles.customer_profile",contact_id=contact_id))
    else:
        return redirect(url_for("profiles.customer_profile",contact_id=contact_id))





















