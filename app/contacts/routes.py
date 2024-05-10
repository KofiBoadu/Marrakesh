from flask import render_template, request, redirect, url_for, session, jsonify
from app.utils.tours import create_new_tour_packages, get_all_destinations, get_destination_id
from app.contacts import contacts_bp
import math
from flask_login import login_required, current_user
from app.utils.main import format_phone_number, all_states, update_contact_owner
from .contact_models import remove_contacts, get_total_num_of_contacts, check_contact_exists, add_new_contact, \
    get_filtered_contacts_count
from .contact_models import update_full_contact_details, get_contact_id, get_all_contacts_information, \
    get_filtered_information
from app.contact_profile.profile_models import fetch_contact_details
from app.utils.main import cache
from app.utils.tours import get_all_tour_names
from app.users.admin_models import get_all_users


@contacts_bp.route('/contacts/home', methods=['GET', 'POST'])
@login_required
def home_page():
    # Extract common parameters from the request
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', default=50, type=int)
    search_query = request.args.get('search_query', '')

    # Prepare user and page data
    login_user = current_user
    login_user_email = login_user.email_address
    username = session.get('username', 'Guest')

    if request.method == 'GET':
        # Fetch data based on the current page, items per page, and search query
        customers = get_all_contacts_information(page, items_per_page, search_query)
        customers_total = get_total_num_of_contacts(search_query)
        total_pages = math.ceil(customers_total / items_per_page)

        # Additional data needed for full page render
        destinations = get_all_destinations()
        states = all_states()
        all_users = get_all_users()
        all_tours = get_all_tour_names()

        # Return full page or JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            table_body_html = render_template('table_body.html', customers=customers)
            pagination_html = render_template('table_paginations.html', page=page, total_pages=total_pages)
            return jsonify({
                'table_body_html': table_body_html,
                'pagination_html': pagination_html,
                'total_records': customers_total
            })

        return render_template("homepage.html", items_per_page=items_per_page, states=states, all_tours=all_tours,
                               login_user_email=login_user_email, customers=customers, destinations=destinations,
                               username=username, customers_total=customers_total, page=page, total_pages=total_pages,
                               all_users=all_users)

    elif request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX POST request processing
        data = request.get_json()
        search_query = data.get('search_query', '')
        print(search_query)
        page = int(data.get('page', 1))
        items_per_page = int(data.get('items_per_page', 50))

        customers = get_all_contacts_information(page, items_per_page, search_query)

        customers_total = get_total_num_of_contacts(search_query)

        total_pages = math.ceil(customers_total / items_per_page)

        return jsonify({
            'html': render_template('table_body.html', customers=customers),
            'total_records': customers_total,
            'pagination_html': render_template('table_paginations.html', page=page, total_pages=total_pages)
        })

    return render_template("error_page.html"), 404


#
# @contacts_bp.route('/contacts/filter', methods=['POST'])
# @login_required
# def filter_contacts():
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         data = request.get_json()
#         status = data.get('status', None)
#         gender = data.get('gender', None)
#         state = data.get('state', None)
#         tour_name = data.get('tour_name', None)
#
#         page = int(data.get('page', 1))
#         items_per_page = int(data.get('items_per_page', 50))
#
#         try:
#             customers = get_filtered_information(page, items_per_page, status, gender, state, tour_name)
#             total_contacts = get_filtered_contacts_count(status, gender, state, tour_name)
#             total_pages = math.ceil(total_contacts / items_per_page)
#
#             html = render_template('table_body.html', customers=customers)
#             pagination_html = render_template('table_paginations.html', page=page, total_pages=total_pages, items_per_page=items_per_page)
#             return jsonify(html=html, total_records=total_contacts, pagination_html=pagination_html)
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500  # Properly handle the error scenario
#     return jsonify({'error': 'Invalid request'}), 400


@contacts_bp.route('/details', methods=['GET'])
@login_required
def get_customer_details():
    customer_id = request.args.get('customer_id')
    print("Requested Customer ID:", customer_id)

    the_details = fetch_contact_details(customer_id)

    if the_details:
        customer = the_details[0]  # Extract the first tuple

        customer_dict = {
            "customer_id": customer[0],
            "first_name": customer[1],
            "last_name": customer[2],
            "state_address": customer[3] if customer[3] is not None else "",
            "email_address": customer[4],
            "phone_number": customer[5]
        }
        return jsonify(customer_dict)
    else:
        return jsonify({"error": "Customer not found"}), 404


@contacts_bp.route('/update_details', methods=['POST'])
@login_required
def send_update():
    customer_id = request.form.get('updatecustomer_id')
    first_name = request.form.get('updatefirst_name')
    last_name = request.form.get('updatelast_name')
    state = request.form.get('updatestate')
    email = request.form.get('updateemail')
    phone = request.form.get('updatephone')
    gender = request.form.get('updategender')

    update_full_contact_details(customer_id, first_name, last_name, email, phone, gender, state)

    return redirect(url_for("contacts.home_page"))


@contacts_bp.context_processor
@login_required
def context_processor():
    return dict(format_phone_number=format_phone_number)


@contacts_bp.route('/delete_contacts', methods=['POST'])
@login_required
def delete_contact():
    customer_ids = request.form.get("customer_id")
    if customer_ids:
        customer_ids = customer_ids.split(',')
        customer_ids = [int(id) for id in customer_ids if id.isdigit()]
        remove_contacts(customer_ids)
        return redirect(url_for("contacts.home_page"))

    else:
        return redirect(url_for("contacts.home_page"))


@contacts_bp.route('/add_customer', methods=['POST'])
@login_required
def adding_new_contact():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        state = request.form.get('state')
        email = request.form.get('email')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        lead_status = request.form.get("lead_status")

        customer_exist = check_contact_exists(email)
        if not customer_exist:
            add_new_contact(first_name, last_name, email, phone, gender, state, lead_status)
            contact_id = get_contact_id(email)
            if contact_id:
                return redirect(url_for("profiles.contact_profile", contact_id=contact_id))


@contacts_bp.route('/add_new_tours', methods=['POST'])
@login_required
def add_new_tours():
    if request.method == 'POST':
        tour_raw_name = request.form.get('name')
        tour_name = " ".join(tour_raw_name.split())
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        tour_price = request.form.get('price')
        destination = request.form.get('destination')
        tour_type = request.form.get('tour_type')
        destination_id = get_destination_id(destination)
        create_new_tour_packages(tour_name, start_date, end_date, tour_price, destination_id, tour_type)
    return redirect(url_for("users.tour_services"))


@contacts_bp.route('/check-email/contact-existence', methods=['POST'])
def validate_contact_existence():
    data = request.get_json()
    email = data.get('email')
    contact_id = check_contact_exists(email)
    if contact_id:
        contact = fetch_contact_details(contact_id)
        contact_details = {
            "exists": True,
            "contact_id": contact[0][0],
            "first_name": contact[0][1],
            "last_name": contact[0][2],
            "email_address": contact[0][4]
        }
        return jsonify(contact_details)
    else:
        return jsonify({'exists': False})


@contacts_bp.route('/contact/owner/assigned', methods=['GET', 'POST'])
def assigning_contact_owner():
    user_id = request.form.get('user_id')
    contact_id = request.form.get('contact_id')
    new_owner_name = update_contact_owner(contact_id, user_id)
    if new_owner_name is not None:
        return jsonify({'owner': new_owner_name})
    else:
        return jsonify({'error': 'Update failed'}), 500
