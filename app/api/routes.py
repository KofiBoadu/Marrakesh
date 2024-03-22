from flask import request, jsonify
from . import api_blueprint
from  .config import auth,create_leads,create_standardized_model,create_submissions,add_submission_data
import logging
from flask import current_app as app
from dotenv import load_dotenv
import os

load_dotenv()




VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')














@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593', methods=['POST'])
def add_new_lead():
    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    else:
        data = request.json
    contact=create_standardized_model(data)

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
            source=contact.get('source')
            submission_id=create_submissions(contact_id,source)

            if submission_id:
                for key,value in contact['form_data'].items():
                    add_submission_data(submission_id,key,value)
        return jsonify({"contact_id": contact_id}),200
    else:
        return jsonify({"error": "Invalid contact data"}),400





@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593/facebook-ads-leads-gen', methods=['GET','POST'])
def face_book_leads():
    if request.method == 'GET':
        # Facebook webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return challenge
            return 'Verification token mismatch', 403
        return 'Bad request', 400

    elif request.method == 'POST':
        # Your logic to handle the lead data
        # ...

        return jsonify(success=True), 200
