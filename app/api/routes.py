from flask import request, jsonify,abort
from . import api_blueprint
from  .config import auth,create_leads,standardized_model_wordpress,create_submissions,add_submission_data,standardized_model_facebook,is_spam
import logging
from flask import current_app as app
from dotenv import load_dotenv
import os
import sys
import hmac
import hashlib
import paypalrestsdk




paypalrestsdk.configure({
  'mode': 'sandbox', # 'sandbox' or 'live'
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
    if is_spam(request_data):
        print("spam")
        abort(400, description="Spam detected")

    token = request.args.get('token')
    if token != SECRET_TOKEN:
        abort(403)

    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        data = request.json
    contact=standardized_model_wordpress(data)

    if contact:
        contact_id = create_leads(
            first_name=contact.get('first_name'),
            last_name=contact.get('last_name'),
            email=contact.get('email'),
            phone=contact.get('phone_number'),
            gender=contact.get('gender'),
            state=contact.get('state')
        )
        if contact_id:
            source="wordpress"
            submission_id=create_submissions(contact_id,source)

            if submission_id:
                for key,value in contact['form_data'].items():
                    add_submission_data(submission_id,key,value)
        return jsonify({"contact_id": contact_id}),200
    else:
        return jsonify({"error": "Invalid contact data"}),400





@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593/facebook-ads-leads-gen', methods=['POST'])
@auth.login_required
def face_book_leads():
    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        data = request.json
    contact=standardized_model_facebook(data)
    if contact:
        contact_id = create_leads(
            first_name=contact.get('first_name'),
            last_name=contact.get('last_name'),
            email=contact.get('email'),
            phone=contact.get('phone_number'),
            gender=contact.get('gender'),
            state=contact.get('state')
        )
        if contact_id:
            source="facebook"
            submission_id=create_submissions(contact_id,source)
            if submission_id:
                for key,value in contact['form_data'].items():
                    add_submission_data(submission_id,key,value)
        return jsonify({"contact_id": contact_id}),200

    else:
        return jsonify({"error": "Invalid contact data"}),400





@api_blueprint.route('/paypal-transactions/23902-marrakesh-customer-payments', methods=['GET','POST'])
def paypal_transactions_records():
    data = request.json
    headers = request.headers


    transmission_id = headers.get('PayPal-Transmission-Id')
    timestamp = headers.get('PayPal-Transmission-Time')
    webhook_id = os.getenv('WEBHOOK_ID')
    event_body = request.get_data(as_text=True) 
    cert_url = headers.get('PayPal-Cert-Url')
    actual_signature = headers.get('PayPal-Transmission-Sig')
    

    response = paypalrestsdk.WebhookEvent.verify(
        transmission_id=transmission_id,
        timestamp=timestamp,
        webhook_id=webhook_id,
        event_body=event_body,
        cert_url=cert_url,
        actual_signature=actual_signature,
    )

    if response:
        print("Webhook verified")
        
       
    else:
        print("Invalid webhook signature")
        
    return jsonify(success=True)

    print(request.json)


    return jsonify("data receieved "),200
    




