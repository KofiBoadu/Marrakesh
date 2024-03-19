from flask import  render_template, request,redirect,url_for,flash
from .import analytics
from app.models import get_total_number_of_travellers,calculate_gross_revenue
import datetime
from app.reports import customers_location_by_state,customers_by_gender,get_travellers_by_destination_query,calculate_annual_gross_revenue
from flask import Flask, jsonify
from app.emails import our_customers_sincebyYear
from flask_login import login_required




@analytics.route('/analytics', methods=['GET'])
@login_required
def analytics_home():
    current_year = datetime.datetime.now().year
   
    total_travelers = get_total_number_of_travellers()
    revenue, formatted_revenue = calculate_gross_revenue(current_year)
    list_years=our_customers_sincebyYear()
    revenue_data= calculate_annual_gross_revenue()
    total_revenue=0
    for year , amount in revenue_data:
        total_revenue=total_revenue+float(amount.replace(',',''))

    total_revenue= "{:.2f}".format(total_revenue)
    return render_template("analytics.html", total_revenue=total_revenue, total_travelers=total_travelers, current_year= current_year, revenue=revenue, formatted_revenue=formatted_revenue,list_years=list_years)




@analytics.route('/location_chart')
@login_required
def customers_location_charts():
    data= customers_location_by_state()
     # Convert the result to a list of dicts to jsonify it
    data_list = [{'state_group': state, 'customer_count': count} for state, count in data]
    return jsonify(data_list)





@analytics.route('/gender_chart')
@login_required
def customers_gender_charts():
    year= request.args.get("gender_year",default=None)
    gender_data= customers_by_gender(year)
    return jsonify(gender_data)



@analytics.route('/revenue_chart')
@login_required
def revenue_charts():
    revenue_data= calculate_annual_gross_revenue()
   
    return jsonify(revenue_data)




@analytics.route('/bookings_chart')
@login_required
def customers_bookings_charts():
    year= request.args.get("bookings_year",default=None)
    bookings_data= get_travellers_by_destination_query(year)
    return jsonify(bookings_data)
