from flask import render_template, request, redirect, url_for,jsonify
from flask_login import login_required, current_user
from .profile_models import updating_contact_status, update_contact_phone, \
    change_contact_bookings, get_contact_activities, updating_contact_state, \
    bookings_updates_logs, update_contact_email, update_contact_name
from .profile_models import save_contact_notes, delete_contacts_notes,get_contact_task
from  app.utils.main  import send_email,all_states,format_phone_number
from app.utils.task_models import generate_due_dates,generate_time_intervals,adding_new_task,update_task_title,update_task_due_date,\
    update_task_due_time,find_matching_interval,update_task_with_new_description,delete_contact_task,timedelta_to_time_str
from app.utils.tours import get_all_upcoming_travel_packages,get_travel_package_id,book_a_tour_for_a_contact
from .profile_models import profile_details, get_customer_bookings, contact_submissions, contact_gender_update
from . import contacts_profile
from app.utils.main import cache



@contacts_profile.route('/<int:contact_id>', methods=['GET'])
@login_required
def contact_profile(contact_id):
    if not contact_id:
        return redirect(url_for("contacts.home_page"))
    else:
        profile = profile_details(contact_id)
        if not profile:
            return redirect(url_for("contacts.home_page"))

        tour_names = profile[6]
        tour_list = tour_names.split(', ') if tour_names else []

        phone_number = format_phone_number(profile[2]) if profile[2] else "Not Provided"

        booking_info = get_customer_bookings(contact_id) if tour_list else []

        available_dates = get_all_upcoming_travel_packages()

        activities = get_contact_activities(contact_id)

        states = all_states()

        results = contact_submissions(contact_id)

        due_dates= generate_due_dates()
        due_dates_names = list(due_dates.keys())
        due_times= generate_time_intervals()

        due_time_options= [ times['value'] for times in due_times]


        contact_tasks=get_contact_task(contact_id)
        time_formats = generate_time_intervals()
        time_intervals = {interval['key']: interval['value'] for interval in time_formats}

        updated_contact_task= []

        for task in contact_tasks:
            time_24hr_format= timedelta_to_time_str(task[3])
            task_list= list(task)
            time_12hr_format= time_intervals.get(time_24hr_format,"not found")
            task_list[3]=time_12hr_format
            updated_contact_task.append(task_list)




        form_fields_dict = {}

        common_data = {}

        if results:
            common_data = {
                'name': f"{results[0][0]} {results[0][1]}",
                'submission_source': results[0][2],
                'submission_date': results[0][3].strftime('%B %d, %Y %I:%M %p')
            }

            for _, _, _, _, field_name, field_value in results:
        
                field_display_name = field_name.replace('_', ' ').title()
                form_fields_dict[field_display_name] = field_value

        login_user = current_user.email_address
        return render_template('profile.html', common_data=common_data, form_fields=form_fields_dict, states=states,
                               activities=activities, available_dates=available_dates, booking_info=booking_info,
                               login_user=login_user, profile=profile, tour_list=tour_list, contact_id=contact_id,due_dates=due_dates,
                               phone_number=phone_number,due_dates_names=due_dates_names,due_time_options=due_time_options,contact_tasks=updated_contact_task)






@contacts_profile.route('/update-customer-reservations', methods=['POST'])
@login_required
def change_bookings():
    contact_id = request.form.get('updatingbooking_contact_id')
    print("ID", contact_id)
    new_tour_type = request.form.get('updatetour_date')
    print("new tour type")
    checkbox_checked = 'notify-customer' in request.form
    customer_details = profile_details(contact_id)

    contact_name = profile_details(contact_id)[0].split()[0].capitalize()
    contact_email = customer_details[1]
    tour_date = new_tour_type.split()
    tour_year = tour_date.pop()
    tour_name = " ".join(tour_date)
    print("new tour name",tour_name)

    old_tour_name = request.form.get("modify_from")
    old_tour_date = old_tour_name.split()
    old_tour_year = old_tour_date.pop()
    new_old_tour_name = " ".join(old_tour_date)

    update_message = f"""Dear {contact_name},

           We have successfully updated your trip from {old_tour_name} to {new_tour_type}

      Warm regards,
      Africa Travellers
    """

    subject = "Tour update"
    if checkbox_checked:
        send_email(subject, [contact_email], update_message)

    new_tour_id = get_travel_package_id(tour_name, tour_year)
    old_tour_id = get_travel_package_id(new_old_tour_name, old_tour_year)

    user_id = current_user.id
    update_details_message = f" Tour was updated from {old_tour_name} to {new_tour_type}"

    bookings_updates_logs(old_tour_id, new_tour_id, contact_id, user_id, update_details_message)

    booking_id = request.form.get('updatingbooking_booking_id')
    change_contact_bookings(booking_id, new_tour_id, contact_id)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))







@contacts_profile.route('/change-contacts-name', methods=['POST'])
@login_required
def customer_name():
    contact_id = request.form.get('contact_id')
    first_name = request.form.get('updatefirst_name')
    last_name = request.form.get('updatelast_name')
    update_contact_name(first_name, last_name, contact_id)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))







@contacts_profile.route('/change-contacts-email', methods=['POST'])
@login_required
def customer_email():
    contact_id = request.form.get('contact_id')
    email = request.form.get('update_email')
    update_contact_email(email, contact_id)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))







@contacts_profile.route('/change-contact-phone', methods=['POST'])
@login_required
def update_contact_phone_number():
    contact_id = request.form.get('contact_id')
    print(contact_id)
    phone = request.form.get('update_phone')
    print(phone)
    update_contact_phone(contact_id, phone)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))





@contacts_profile.route('/update_customer_state', methods=['POST'])
@login_required
def update_state_of_contact():
    contact_id = request.form.get('contact_id')
    new_state = request.form.get('new_state')
    updating_contact_state(new_state, contact_id)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))





@contacts_profile.route('/notes', methods=['POST'])
@login_required
def contact_notes():
    contact_id = request.form.get('contact_id')
    contact_note = request.form.get('notes')
    note_creator = current_user.first_name + " " + current_user.last_name
    save_contact_notes(contact_id, contact_note, note_creator)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))




@contacts_profile.route('/delete_notes', methods=['POST'])
@login_required
def deleting_contact_notes():
    notes_id = request.form.get('notes_id')
    contact_id = request.form.get('contact_id')
    delete_contacts_notes(notes_id, contact_id)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))





@contacts_profile.route('/change-contact-status', methods=['POST'])
@login_required
def new_contact_status():
    contact_id = request.form.get('contact_id')
    new_status = request.form.get('new_contact_status_name')
    updating_contact_status(new_status, contact_id)
    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))






@contacts_profile.route('/making-tour-reservation', methods=['POST'])
@login_required
def confirm_contact_tour_bookings():
    contact_id = request.form.get('contact_id')
    selected_tour = request.form.get('tour_date')
    print("selected_tour", selected_tour)
    profile = profile_details(contact_id)
    if contact_id and selected_tour:
        tour_date = selected_tour.split()
        print("tour_date", tour_date)
        tour_year = tour_date.pop()
        tour_name = " ".join(tour_date)
        print("tour_name", tour_name)
        tour_id = get_travel_package_id(tour_name, tour_year)
        print("tour id",tour_id)
        book_a_tour_for_a_contact(tour_id, contact_id)
        if profile[4] != "customer":
            new_status = "customer"
            updating_contact_status(new_status, contact_id)
        return redirect(url_for("profiles.contact_profile", contact_id=contact_id))
    else:
        return redirect(url_for("profiles.contact_profile", contact_id=contact_id))






@contacts_profile.route('/update-contact=gender', methods=['POST'])
@login_required
def update_contact_gender():
    contact_id = request.form.get('contact_id')
    gender = request.form.get('new_gender')
    if contact_id:
        contact_gender_update(contact_id, gender)
        return redirect(url_for("profiles.contact_profile", contact_id=contact_id))
    else:
        print("there was an issue with updating the gender")
        return redirect(url_for("profiles.contact_profile", contact_id=contact_id))



@contacts_profile.route('/creating_task', methods=['POST'])
def creating_new_task():
    task_title = request.form.get('taskTitle')
    custom_date = request.form.get('customDueDate')
    due_date_value = generate_due_dates()
    date = ""
    if custom_date:
        date = custom_date
        print(f"Custom date used: {custom_date}")

    else:
        due_date = request.form.get('dueDate')
        if due_date:
            date = due_date_value[due_date]["date"]
            print(f"Predefined date used: {date}")
        else:
            print(f"Invalid date selected: {due_date}")


    due_time = request.form.get('dueTime')
    time_formats= generate_time_intervals()
    time_intervals={interval['value']: interval['key'] for interval in time_formats}
    due_time_24= time_intervals.get(due_time)

    task_description = request.form.get('notes')
    contact_id = request.form.get('contact_num')
    user_id = current_user.id

    if contact_id and user_id:
        print("Contact ID:", contact_id)  # Debug: Check what's captured
        adding_new_task(task_title, date, due_time_24, task_description, contact_id,user_id)
    else:
        print("No contact ID provided")  # Debug: Identify if no ID is captured

    return redirect(url_for("profiles.contact_profile", contact_id=contact_id))



@contacts_profile.route('/update_task_title/', methods=['POST'])
def add_new_task_title():
    task_new_title= request.form.get('taskTitle')
    new_task_id= request.form.get('task_id')
    if new_task_id and task_new_title:
        success = update_task_title(new_task_id, task_new_title)
        return jsonify({'success': success}), 200
    return jsonify({'success': False}), 400


@contacts_profile.route('/update_task/due_date',methods=['POST'])
def add_new_task_due_date():
    custom_date= request.form.get('update-customDueDate')
    due_date_value = generate_due_dates()
    task_id=request.form.get('task_id')
    if custom_date:
        new_custom_date= custom_date
        success=update_task_due_date(new_custom_date, task_id)
        return jsonify({'success': success}), 200
    due_date = request.form.get('update-dueDate')
    if due_date:
        selected_date = due_date_value[due_date]["date"]
        if task_id and selected_date:
            success=update_task_due_date(selected_date,task_id)
            return jsonify({'success': success}), 200
    return jsonify({'success': False}), 400



@contacts_profile.route('/update_task_due_time/new_time',methods=['POST'])
def updating_task_new_due_time():
    new_due_time= request.form.get("update-due-time")
    task_id= request.form.get("task_id")
    time_formats = generate_time_intervals()
    time_intervals = {interval['value']: interval['key'] for interval in time_formats}
    new_time_24hrs= time_intervals.get(new_due_time)
    if new_due_time and task_id:
        success=update_task_due_time(new_time_24hrs, task_id)
        return jsonify({'success': success}), 200
    return jsonify({'success': False}), 400


@contacts_profile.route('/update_task/description',methods=['POST'])
def update_new_task_description():
    new_task_description= request.form.get("task-description")
    task_id= request.form.get("task_id")
    if new_task_description and task_id:
        success= update_task_with_new_description(new_task_description,task_id)
        return jsonify({'success': success}), 200
    else:
        return jsonify({'success': False}),  400


@contacts_profile.route('/delete/contact/task',methods=['POST'])
def delete_a_task():
    task_id= request.form.get("task_id")
    contact_id= request.form.get("contact_id")
    if task_id and contact_id:
        delete_contact_task(task_id)
        return redirect(url_for("profiles.contact_profile", contact_id=contact_id))
