from flask import request, jsonify
from . import api_blueprint
from  .config import auth,create_leads
import logging
from flask import current_app as app







# webhook url
# https://africatravellers-crm-7ca32dc61ea0.herokuapp.com/api/adding-new-lead-3e7a8f9d-94593
 # Ensure you import your Flask app and blueprint correctly

@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593', methods=['POST'])
def add_new_lead():
    print("Received new lead request")

    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form.to_dict()
    elif request.content_type == 'application/json':
        data = request.json
    else:
        print("Unsupported Media Type:", request.content_type)
        return jsonify({"success": False, "error": "Unsupported Media Type"}), 415

    # Normalize keys of incoming data
    normalized_data = {key.strip().replace(' ', '_').lower(): value for key, value in data.items()}
    print("Normalized Form data:", normalized_data)

    # Mapping of normalized form field names to your expected field names
    field_mappings = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',  # Assume the normalized key is exactly 'email'
        'phone_number': 'phone',  # Corresponds to 'Phone Number' after normalization
        'gender': 'gender',  # Adjust as needed based on your form's actual keys
        'state': 'state'  # Adjust as needed
    }

    # Prepare data with mapped keys using normalized data
    processed_data = {}
    for form_key, internal_key in field_mappings.items():
        # Use None for fields that are empty or not provided
        processed_data[internal_key] = normalized_data.get(form_key) or None

    print("Processed data before validation:", processed_data)

    required_fields = ['first_name', 'last_name', 'email']
    missing_fields = [field for field in required_fields if not processed_data.get(field)]

    if missing_fields:
        print("Missing required fields:", missing_fields)
        return jsonify({"success": False, "error": f"Missing required data for fields: {', '.join(missing_fields)}"}), 400

    try:
        # Assuming create_leads is a function defined elsewhere in your code that
        # creates a new lead in your database or CRM system.
        contact_row_id = create_leads(**processed_data)
        print("Lead created successfully with ID:", contact_row_id)
        return jsonify({"success": True, "message": "Lead created successfully", "customer_row_id": contact_row_id}), 200

    except Exception as e:
        print("Failed to create lead:", str(e))
        app.logger.error(f"Failed to create lead: {str(e)}")  # Log the error for debugging
        return jsonify({"success": False, "error": "Failed to process the request"}), 500
