from flask import  render_template, request,redirect,url_for,flash
from . import analytics
from app.models import get_total_numberOfTravellers,calculate_gross_revenue
import datetime
from app.reports import customers_location_by_state
from flask import Flask, jsonify





@analytics.route('/analytics', methods=['GET'])
def analytics_home():
    year = datetime.datetime.now().year
    total_travelers = get_total_numberOfTravellers()
    revenue, formatted_revenue = calculate_gross_revenue(year)
    return render_template("analytics.html", total_travelers=total_travelers, year=year, revenue=revenue, formatted_revenue=formatted_revenue)




@analytics.route('/location_chart')
def customers_location_charts():
    data= customers_location_by_state()
     # Convert the result to a list of dicts to jsonify it
    data_list = [{'state_group': state, 'customer_count': count} for state, count in data]
    return jsonify(data_list)


