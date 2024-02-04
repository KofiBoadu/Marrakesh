from flask import  render_template, request,redirect,url_for,flash
from . import email_marketing
from app.user import get_all_users
from app.emails import our_customers_sincebyYear,get_customers_by_year_or_all,mass_send_emailTemplate
import asyncio



@email_marketing.route('/emails', methods=['GET'])
def marketing_emails():
    return render_template("email_marketing.html")



@email_marketing.route('/sending-emails', methods=['GET', 'POST'])
def create_marketingEmails():
    if request.method == 'POST':

        from_address=request.form.get('fromAddress'),
        email_subject=request.form.get('emailSubject')
        email_body=request.form.get('emailBody'),
        email_list=[("daniel", "mrboadu3@gmail.com"), ("kofi", "bookings@africatravellers.com")]
        d_email_list = email_list * 100
        

        asyncio.run(mass_send_emailTemplate(email_subject, from_address, d_email_list, email_body))
       
        return redirect(url_for("marketing.marketing_emails"))

    senders = get_all_users()
    customer_list_byYear = our_customers_sincebyYear()
    return render_template("sendEmail_marketing.html", senders=senders, customer_list_byYear=customer_list_byYear)




