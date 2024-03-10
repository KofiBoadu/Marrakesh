from flask import  render_template, request,redirect,url_for,flash
from . import email_marketing
from  app.mass_email_marketing import send_emails_asynchronously
from app.user import get_all_users
from app.emails import our_customers_sincebyYear,get_customers_by_year_or_all
from app.mass_email_marketing import marketing_Email,all_email_campaign
from flask_login import login_required, current_user


@email_marketing.route('/emails', methods=['GET'])
@login_required
def marketing_emails():
    campaigns= all_email_campaign()
    return render_template("email_marketing.html",campaigns=campaigns)



@email_marketing.route('/sending-emails', methods=['GET', 'POST'])
@login_required
def create_marketingEmails():
    if request.method == 'POST':

        from_address=request.form.get('fromAddress')
        email_subject=request.form.get('emailSubject')
        email_body=request.form.get('emailBody')
        email_list=[("daniel", "mrboadu3@gmail.com")] * 10
        user_id=current_user.id
        # d_email_list = email_list * 90


       
        send_emails_asynchronously(email_list, email_subject, from_address, email_body)
        # Now, insert campaign details into the database
        marketing_Email(
            user_id=user_id,
            total_email_list=len(email_list),
            campaign_subject=email_subject,
            campaign_body=email_body,
            campaign_status="sent"
        )

        return redirect(url_for("marketing.marketing_emails"))

    senders = get_all_users()
    customer_list_byYear = our_customers_sincebyYear()
    return render_template("sendEmail_marketing.html", senders=senders, customer_list_byYear=customer_list_byYear)




