from flask import  render_template, request,redirect,url_for,flash,session
from app.models import get_customers_information, available_tour_dates,add_new_paidCustomer,get_destination_id
from app.models import get_tour_id,get_customer_id,create_tour_bookings,get_all_destination,create_new_tourDates
from app.models import check_customer_exists
from app.customers import customers_bp
import datetime
import math
from flask_login import login_required,current_user
from app.extension import cache
from app.models import format_phone_number, remove_paid_customer,total_customers
from app.customer_models import fetch_customer_details,update_customerDetails,update_tour_bookings
from flask import jsonify



@customers_bp.route('/', methods=['GET','POST'])
@login_required
# @cache.cached(timeout=240)
def home_page():
    if request.method == 'GET' or request.method=="POST":
        login_user=current_user
        login_user_email=login_user.email_address
        page = request.args.get('page', 1, type=int)
        search= request.form.get('search_query')
        items_per_page = 50
        username = session.get('username', 'Guest')
        year= datetime.datetime.now().year
        customers= get_customers_information(page, items_per_page,search)
        available_dates= available_tour_dates()
        destinations= get_all_destination()
        
        customers_total=total_customers()
        total_pages = math.ceil(customers_total / items_per_page)
        return render_template("homepage.html",login_user_email=login_user_email,customers=customers,available_dates=available_dates,destinations=destinations,username=username,customers_total=customers_total,page=page, total_pages=total_pages)





@customers_bp.route('/details', methods=['GET'])
def get_customer_details():
    customer_id = request.args.get('customer_id')
    print("Requested Customer ID:", customer_id)
    
    # Fetching customer details from the database
    the_details = fetch_customer_details(customer_id)
  
    
    # Assuming the_details is a list of tuples and we're interested in the first tuple
    if the_details:
        customer = the_details[0]  # Extract the first tuple
        # Convert tuple to dictionary for JSON response
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







@customers_bp.route('/update_details', methods=['POST'])
def send_update():
    customer_id= request.form.get('updatecustomer_id')
    first_name = request.form.get('updatefirst_name')
    last_name = request.form.get('updatelast_name')
    state = request.form.get('updatestate')
    email = request.form.get('updateemail')
    phone = request.form.get('updatephone')
    gender = request.form.get('updategender')
    # tour_type= request.form.get("updatetour_date")
    update_customerDetails(customer_id, first_name, last_name,email ,phone, gender, state)
    # tour_date= tour_type.split()
    # tour_year= tour_date.pop()
    # tour_name=" ".join(tour_date)
    # tour_id= get_tour_id(tour_name,tour_year)
    # update_tour_bookings(tour_id, customer_id)
    return redirect(url_for("customers.home_page"))





@customers_bp.context_processor
def context_processor():
    return dict(format_phone_number=format_phone_number)




@customers_bp.route('/delete_customer',methods=['POST'])
def delete_customer():
    customer_id= request.form.get("customer_id")
    if not customer_id:
        return redirect(url_for("customers.home_page"))
    else:
        remove_paid_customer(customer_id)
        return redirect(url_for("customers.home_page"))






@customers_bp.route('/add_customer', methods=['POST'])
@login_required
def add_paid_customer():
    if request.method=='POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        state = request.form.get('state')
        email = request.form.get('email')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        tour_type= request.form.get("tour_date")

        tour_date= tour_type.split()
        print(tour_date)

        customer_exist=check_customer_exists(email)
        print(customer_exist)

        tour_year= tour_date.pop()
        print(tour_year)

        tour_name=" ".join(tour_date)
        print(tour_name)

        tour_id= get_tour_id(tour_name,tour_year)
        print(tour_id)


        if customer_exist:
            customer_id= customer_exist
            tour_id= get_tour_id(tour_name,tour_year)
            create_tour_bookings(tour_id,customer_id)
            return redirect(url_for("customers.home_page"))
        else:
            customer= add_new_paidCustomer(first_name, last_name,email,phone,gender,state)
            tour_id= get_tour_id(tour_name,tour_year)
            customer_id= get_customer_id(email)
            create_tour_bookings(tour_id,customer_id)
            return redirect(url_for("customers.home_page"))







@customers_bp.route('/add_new_tours',methods=['POST'])
@login_required
def add_new_tours():
    if request.method=='POST':
        tour_name = request.form.get('name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        tour_price= request.form.get('price')
        destination = request.form.get('destination')
        tour_type=request.form.get('tour_type')
        destination_id= get_destination_id(destination)
        create_new_tourDates(tour_name, start_date,end_date,tour_price,destination_id, tour_type)

    return redirect(url_for("customers.home_page"))


