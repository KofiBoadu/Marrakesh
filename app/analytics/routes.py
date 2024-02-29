from flask import  render_template, request,redirect,url_for,flash
from . import analytics
from app.models import get_total_numberOfTravellers,calculate_gross_revenue
import datetime






@analytics.route('/analytics', methods=['GET'])
def analytics_home():
    year = datetime.datetime.now().year
    total_travelers = get_total_numberOfTravellers()
    revenue, formatted_revenue = calculate_gross_revenue(year)
    return render_template("analytics.html", total_travelers=total_travelers, year=year, revenue=revenue, formatted_revenue=formatted_revenue)

# @analytics.route('/analytics',methods=['GET'])
# def analytics_home():
# 	year= datetime.datetime.now().year
# 	total_travelers= get_total_numberOfTravellers()
#     revenue,formatted_revenue= calculate_gross_revenue(year)
# 	return render_template ("analytics.html",total_travelers=total_travelers,year=year,revenue=revenue)