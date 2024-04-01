from flask import request, jsonify, abort
from . import api_blueprint
from .config import auth, create_new_leads, standardized_model_wordpress, create_new_form_submission, \
    add_new_form_submission_data, \
    standardized_model_facebook, is_spam
import os
import paypalrestsdk
from app.models import check_contact_exists

paypalrestsdk.configure({
    'mode': 'live',
    'client_id': os.getenv('PAYPAL_CLIENT_ID'),
    'client_secret': os.getenv('PAYPAL_CLIENT_SECRET')
})

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
APP_SECRET = os.environ.get('APP_SECRET')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')

spammy_patterns = {
    "number_of_days": "8444",
    "number_of_people": "1779",
    "from_date": "1987-01-04",
    "to_date": "1981-07-06",
    "budget": "59301",
    "accommodation_type": "Standard Hotels",
    "destination": "Egypt",
    "first_name": "Williamciz",
    "last_name": "WilliamcizXP",
    "email": "qsudfkjmzfqnejvj@onet.pl",
    "phone_number": "88926932618",
    "message": "узнать больше Футбольный аналитик"
}


@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593', methods=['POST'])
def add_new_lead():
    request_data = request.form.to_dict()
    source = "wordpress"
    # if is_spam(request_data):
    #     print("spam")
    #     abort(400, description="Spam detected")
    #
    # spam_status, reasons = is_spam(request_data)
    # if spam_status:
    #     print(f"Submission flagged as spam for the following reasons: {reasons}")
    #     # Handle spam submission accordingly
    # else:
    #     print("Submission not flagged as spam.")

    # token = request.args.get('token')
    # if token != SECRET_TOKEN:
    #     abort(403)

    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
        print(data)
    else:
        data = request.json

    contact = standardized_model_wordpress(data)
    contact_email = contact.get('email')
    check_if_contact_exist = check_contact_exists(contact_email)
    if check_if_contact_exist:
        existing_contact_id = check_if_contact_exist
        submission_id = create_new_form_submission(existing_contact_id, source)
        if submission_id:
            for key, value in contact['form_data'].items():
                add_new_form_submission_data(submission_id, key, value)
        return jsonify({"submission_id": submission_id}), 200

    else:

        if contact:
            contact_id = create_new_leads(
                first_name=contact.get('first_name'),
                last_name=contact.get('last_name'),
                email=contact.get('email'),
                phone=contact.get('phone_number'),
                gender=contact.get('gender'),
                state=contact.get('state')
            )
            if contact_id:
                submission_id = create_new_form_submission(contact_id, source)
                if submission_id:
                    for key, value in contact['form_data'].items():
                        add_new_form_submission_data(submission_id, key, value)
            return jsonify({"contact_id": contact_id}), 200
        else:
            return jsonify({"error": "Invalid contact data"}), 400





@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593/facebook-ads-leads-gen', methods=['POST'])
@auth.login_required
def face_book_leads():
    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        data = request.json
    contact = standardized_model_facebook(data)
    if contact:
        contact_id = create_new_leads(
            first_name=contact.get('first_name'),
            last_name=contact.get('last_name'),
            email=contact.get('email'),
            phone=contact.get('phone_number'),
            gender=contact.get('gender'),
            state=contact.get('state')
        )
        if contact_id:
            source = "facebook"
            submission_id = create_new_form_submission(contact_id, source)
            if submission_id:
                for key, value in contact['form_data'].items():
                    add_new_form_submission_data(submission_id, key, value)
        return jsonify({"contact_id": contact_id}), 200

    else:
        return jsonify({"error": "Invalid contact data"}), 400
