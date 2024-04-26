import logging
import math
from flask import render_template, request, redirect, url_for, jsonify,current_app
from . import email_marketing
from app.users.admin_models import get_all_users
from app.utils.main import our_customers_since_by_year, get_customers_by_year_or_all,cache
from .mass_email_marketing import marketing_email, all_email_campaign, campaign_open_rate, get_unique_opens,get_email_campaign_subject
from flask_login import login_required, current_user
import app.marketing.mass_email_marketing as market


@email_marketing.route('/emails', methods=['GET'])
@login_required
def marketing_emails():
    campaigns = all_email_campaign()
    total_campaigns=len(campaigns)
    return render_template("email_campaigns.html", campaigns=campaigns,total_campaigns=total_campaigns)



@email_marketing.route('/campaign/performance/<int:campaign_id>', methods=['GET'])
@login_required
def email_campaign_performance(campaign_id):
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    open_rate = campaign_open_rate(campaign_id)
    unique_opens = get_unique_opens(campaign_id)
    total_opens = market.get_total_opens(campaign_id)
    click_rate = market.get_click_rate(campaign_id)
    unique_clicks = market.get_unique_clicks(campaign_id)
    total_clicks = market.get_total_clicks(campaign_id)

    total_emails_sent = market.total_email_list(campaign_id)
    total_pages = math.ceil(total_emails_sent / items_per_page)

    events = market.get_customer_campaign_events(campaign_id, page, items_per_page)

    event_metrics = market.get_event_metrics(campaign_id)

    campaign_subject = get_email_campaign_subject(campaign_id)

    

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
       
        
        table_body_html=render_template('performance_table_body.html', events=events,page=page, total_pages=total_pages, campaign_id=campaign_id)
        pagination_html= render_template('marketing_pagination.html', page=page, total_pages=total_pages, campaign_id=campaign_id)
      

    
    
        return jsonify({
            'marketing_table_body_html': table_body_html,
            'marketing_pagination_html':pagination_html
            })

    else:


        return render_template("campaign_performance.html",
                           page=page,
                           total_pages=total_pages,
                           events=events,
                           total_emails_sent=total_emails_sent,
                           click_events={'click_rate': click_rate, 'unique_clicks': unique_clicks, "total_clicks": total_clicks},
                           campaign_id=campaign_id,
                           open_rate=open_rate,
                           unique_opens=unique_opens,
                           total_opens=total_opens,
                           campaign_subject=campaign_subject,
                           **event_metrics)

    








@email_marketing.route('/sending-marketing-emails/sending-email-campaign/', methods=['GET', 'POST'])
def send_marketing_emails():
    if request.method == "POST":
        data = request.json
        print("Received POST data:", data)

        from_address = data['fromAddress']
        contacts_type = data['customerType']
        email_subject = data['emailSubject']
        email_body = data['emailBody']
        user_id = current_user.id
        # recipient_list = get_customers_by_year_or_all(contacts_type)
        email_list = [('daniel', "mrboadu3@gmail.com"), ('kofi', "kboadu16@gmail.com")]

        print(f"From address: {from_address}, Contacts type: {contacts_type}, Email subject: {email_subject}, Email body: {email_body[:50]}, User ID: {user_id}")

        campaign_id = marketing_email(

            user_id=user_id,
            total_number_of_email_list=len(email_list),
            campaign_subject=email_subject,
            campaign_body=email_body,
            campaign_status="sent"
        )

        print("Campaign ID returned:", campaign_id)
        try:
            if campaign_id:
                print("Enqueuing email tasks...")
                market.enqueue_email_task(email_list, email_subject, from_address, email_body, campaign_id)
                performance_url = url_for('marketing.email_campaign_performance',campaign_id=campaign_id) + "?message=email_processing" + "&campaign_id=" + str(campaign_id)
                print("Redirect URL:", performance_url)
                return jsonify({"message": "Email tasks queued for sending", "redirectUrl": performance_url})
            else:
                logging.error("Failed to create campaign entry in the database.")
                return jsonify({"error": "Failed to create campaign entry in the database."}),500
        except Exception as e:
            logging.error(f"Error queuing marketing emails: {e}")
            return jsonify(
                {"error": "An error occurred while queuing marketing emails.", "redirectUrl": "/marketing/emails"}), 500
    else:
        senders = get_all_users()
        customer_list_by_year = our_customers_since_by_year()
        print("Senders and customer list retrieved for GET request.")
        return render_template("send_marketing_email.html", senders=senders, customer_list_byYear=customer_list_by_year)







@email_marketing.route('/campaign/delete/', methods=['POST'])
@login_required
def delete_email_campaign():
    campaign_id = request.form.get('deleting-campaign_id')
    if campaign_id:
        market.delete_campaign(campaign_id)

    return redirect(url_for("marketing.marketing_emails"))
