from flask import request, jsonify
from . import api_blueprint
from  .config import auth,create_leads






@api_blueprint.route('/adding-new-lead-3e7a8f9d-94593', methods=['POST'])
def add_new_lead():
    data = request.json
    required_fields = ['first_name', 'last_name', 'email']
    missing_fields = []

    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        return jsonify({"success": False, "error": f"Missing required data for fields: {missing_fields}"}), 400

    # Get required fields
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    # Get optional fields, these will be None if not provided
    phone = data.get('phone')
    gender = data.get('gender')
    state = data.get('state')

    try:
        customer_row_id = create_leads(first_name, last_name, email, phone, gender, state=state)
        return jsonify({"success": True, "customer_row_id": customer_row_id}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
