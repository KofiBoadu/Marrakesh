from flask import request, jsonify
from . import api_blueprint
from  .config import auth,create_leads
import logging
from flask import current_app as app




# @api_blueprint.route('/adding-new-lead-3e7a8f9d-94593', methods=['POST'])
# def add_new_lead():

#     if request.content_type == 'application/x-www-form-urlencoded':
#         # Convert the form data to a Python dictionary
#         data = request.form.to_dict()
#     elif request.content_type == 'application/json':
#         # Directly get JSON data if the correct content type header is set
#         data = request.json
#     else:
#         # If neither, return a 415 unsupported media type
#         return jsonify({"success": False, "error": "Unsupported Media Type"}), 415

#     required_fields = ['first_name', 'last_name', 'email']

#     missing_fields = []

#     # Check if all required fields are present
#     for field in required_fields:
#         if field not in data:
#             missing_fields.append(field)

#     if missing_fields:
#         return jsonify({"success": False, "error": f"Missing required data for fields: {missing_fields}"}), 400

#     # Get required fields
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     email = data.get('email')

#     # Get optional fields, these will be None if not provided
#     phone = data.get('phone')
#     gender = data.get('gender')
#     state = data.get('state')

#     try:
#         customer_row_id = create_leads(first_name, last_name, email, phone, gender, state=state)
#         return jsonify({"success": True, "customer_row_id": customer_row_id}), 201
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500






@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593', methods=['POST'])
def add_new_lead():
    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    elif request.content_type == 'application/json':
        data = request.json
    else:
        return jsonify({"success": False, "error": "Unsupported Media Type"}), 415

    # Mapping of form field names to your expected field names
    field_mappings = {
        'First Name': 'first_name',
        'Last Name': 'last_name',
        'Email ': 'email',  # Note the trailing space in the form's 'Email ' field
        'Phone Number': 'phone',
        'Gender': 'gender',
        'State': 'state'
    }

    # Prepare data with mapped keys
    processed_data = {}
    for form_key, internal_key in field_mappings.items():
        # Strip to clean spaces and use None for fields that are empty or not provided
        processed_data[internal_key] = data.get(form_key, '').strip() or None

    required_fields = ['first_name', 'last_name', 'email']
    missing_fields = [field for field in required_fields if not processed_data.get(field)]

    if missing_fields:
        return jsonify({"success": False, "error": f"Missing required data for fields: {', '.join(missing_fields)}"}), 400

    try:
        # Assuming create_leads function signature matches these field names
        customer_row_id = create_leads(**processed_data)
        return jsonify({"success": True, "customer_row_id": customer_row_id}), 201
    except Exception as e:
        app.logger.error(f"Failed to create lead: {str(e)}")  # Log the error for debugging
        return jsonify({"success": False, "error": "Failed to process the request"}), 500
