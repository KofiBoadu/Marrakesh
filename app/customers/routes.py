from flask import  render_template, request,redirect,url_for,flash,session
from app.models import get_customers_information, available_tour_dates,add_new_paidCustomer,get_destination_id
from app.models import get_tour_id,get_customer_id,create_tour_bookings,get_all_destination,create_new_tourDates
from app.models import check_customer_exists,get_total_numberOfTravellers,calculate_gross_revenue
from app.customers import customers_bp
import datetime
import math
from flask_login import login_required
from app.extension import cache
from app.models import format_phone_number, remove_paid_customer,total_customers





@customers_bp.route('/', methods=['GET'])
@login_required
# @cache.cached(timeout=240)
def home_page():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        items_per_page = 8
        username = session.get('username', 'Guest')
        year= datetime.datetime.now().year
        customers= get_customers_information(page, items_per_page)
        available_dates= available_tour_dates()
        destinations= get_all_destination()
        total_travelers= get_total_numberOfTravellers()
        revenue= calculate_gross_revenue(year)
        customers_total=total_customers()
        total_pages = math.ceil(customers_total / items_per_page)
        return render_template("homepage.html",customers=customers,available_dates=available_dates,destinations=destinations,total_travelers=total_travelers,year=year,revenue=revenue,username=username,customers_total=customers_total,page=page, total_pages=total_pages)



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

        print(tour_type)

        tour_date= tour_type.split()

        print("Tour date",tour_date)

        customer_exist=check_customer_exists(email)

        tour_year= tour_date.pop()

        print("Tour year", tour_year)

        tour_name=" ".join(tour_date)

        print("tour name", tour_name)

        tour_id= get_tour_id(tour_name,tour_year)

        print("tour ID",tour_id)




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


