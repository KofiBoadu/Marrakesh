from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.contacts_models import updating_contact_status, update_contact_phone, \
    change_contact_bookings, get_contact_activities, updating_contact_state, \
    bookings_updates_logs, update_contact_email, update_contact_name
from app.contacts_notes import save_contact_notes, delete_contacts_notes
from app.emails import send_email
from app.models import book_a_tour_for_a_contact, format_phone_number, get_all_upcoming_travel_packages, \
    get_travel_package_id, all_states
from app.profile_models import profile_details, get_customer_bookings, contact_submissions, contact_gender_update

from . import contacts_profile


@contacts_profile.route('/<int:contact_id>', methods=['GET'])
@login_required
def contact_profile(contact_id):
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

        available_dates = get_all_upcoming_travel_packages()

        activities = get_contact_activities(contact_id)

        states = all_states()

        results = contact_submissions(contact_id)

        # known_field = known_fields

        # form_fields_dict = {field: '' for field in known_field }
        form_fields_dict = {}

        common_data = {}

        if results:
            common_data = {
                'name': f"{results[0][0]} {results[0][1]}",
                'submission_source': results[0][2],
                'submission_date': results[0][3].strftime('%B %d, %Y %I:%M %p')
            }

            for _, _, _, _, field_name, field_value in results:
                # if field_name in known_field:
                field_display_name = field_name.replace('_', ' ').title()
                form_fields_dict[field_display_name] = field_value

        login_user = current_user.email_address
        return render_template('profile.html', common_data=common_data, form_fields=form_fields_dict, states=states,
                               activities=activities, available_dates=available_dates, booking_info=booking_info,
                               login_user=login_user, profile=profile, tour_list=tour_list, contact_id=contact_id,
                               phone_number=phone_number)


@contacts_profile.route('/update-customer-reservations', methods=['POST'])
@login_required
def change_bookings():
    contact_id = request.form.get('updatingbooking_contact_id')
    print("ID", contact_id)
    new_tour_type = request.form.get('updatetour_date')
    checkbox_checked = 'notify-customer' in request.form
    customer_details = profile_details(contact_id)

    contact_name = profile_details(contact_id)[0].split()[0].capitalize()
    contact_email = customer_details[1]
    tour_date = new_tour_type.split()
    tour_year = tour_date.pop()
    tour_name = " ".join(tour_date)

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
    profile = profile_details(contact_id)
    if contact_id and selected_tour:
        tour_date = selected_tour.split()
        tour_year = tour_date.pop()
        tour_name = " ".join(tour_date)
        tour_id = get_travel_package_id(tour_name, tour_year)
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
