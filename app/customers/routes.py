from flask import  render_template, request,redirect,url_for,flash
from app.models import get_customers_information, available_tour_dates,add_new_paidCustomer,get_destination_id
from app.models import get_tour_id,get_customer_id,create_tour_bookings,get_all_destination,create_new_tourDates
from app.models import check_customer_exists
from app.customers import customers_bp
import datetime



@customers_bp.route('/', methods=['GET'])
def home_page():
    if request.method == 'GET':
        year= datetime.datetime.now().year
        customers= get_customers_information(year)
        available_dates= available_tour_dates()
        destinations= get_all_destination()
        return render_template("homepage.html",customers=customers,available_dates=available_dates,destinations=destinations)





@customers_bp.route('/add_customer', methods=['POST'])
def add_paid_customer():
    if request.method=='POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        state = request.form.get('state')
        email = request.form.get('email')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        tour_type= request.form.get("tour_date")
        customer_exist=check_customer_exists(email)

        if customer_exist:
            customer_id= customer_exist
            tour_id= get_tour_id(tour_type)
            create_tour_bookings(tour_id,customer_id)
            return redirect(url_for("customers.home_page"))

        else:
            customer= add_new_paidCustomer(first_name, last_name,email,phone,gender,state)
            tour_id= get_tour_id(tour_type)
            customer_id= get_customer_id(email)
            create_tour_bookings(tour_id,customer_id)
    return redirect(url_for("customers.home_page"))






@customers_bp.route('/add_new_tours',methods=['POST'])
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


