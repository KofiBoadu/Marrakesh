from flask import request, jsonify
from . import api_blueprint
from  .config import auth,create_leads
import logging
from flask import current_app as app




@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593', methods=['POST'])
def add_new_lead():
    app.logger.debug(f"Content-Type: {request.content_type}")

    form_data = {key: value for key, value in request.form.items()}
    app.logger.debug(f"Form Data: {form_data}")
    return jsonify(success=True), 200
    # logging.debug(f"Request data: {request.data}")
    # logging.debug(f"Form data: {request.form}")
    # logging.debug(f"JSON data: {request.json}")
    # if request.content_type == 'application/x-www-form-urlencoded':
    #     # Convert the form data to a Python dictionary
    #     data = request.form.to_dict()
    # elif request.content_type == 'application/json':
    #     # Directly get JSON data if the correct content type header is set
    #     data = request.json
    # else:
    #     # If neither, return a 415 unsupported media type
    #     return jsonify({"success": False, "error": "Unsupported Media Type"}), 415

    # required_fields = ['first_name', 'last_name', 'email']

    # missing_fields = []

    # # Check if all required fields are present
    # for field in required_fields:
    #     if field not in data:
    #         missing_fields.append(field)

    # if missing_fields:
    #     return jsonify({"success": False, "error": f"Missing required data for fields: {missing_fields}"}), 400

    # # Get required fields
    # first_name = data.get('first_name')
    # last_name = data.get('last_name')
    # email = data.get('email')

    # # Get optional fields, these will be None if not provided
    # phone = data.get('phone')
    # gender = data.get('gender')
    # state = data.get('state')

    # try:
    #     customer_row_id = create_leads(first_name, last_name, email, phone, gender, state=state)
    #     return jsonify({"success": True, "customer_row_id": customer_row_id}), 201
    # except Exception as e:
    #     return jsonify({"success": False, "error": str(e)}), 500
