from flask import request, jsonify
from . import api_blueprint
from  .config import auth,create_leads







@api_blueprint.route('/adding-new-lead',methods=['POST'])
@auth.login_required
def add_new_lead():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    gender = data.get('gender')
    state = data.get('state')
    try:
        customer_row_id = create_leads(first_name, last_name, email, phone, gender, state=state)
        return jsonify({"success": True, "customer_row_id": customer_row_id}), 201
    except Exception as e:

        return jsonify({"success": False, "error": str(e)}), 500

