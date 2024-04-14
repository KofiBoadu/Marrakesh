import logging
import math
from flask import render_template, request, redirect, url_for, jsonify
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
    return render_template("email_campaigns.html", campaigns=campaigns)


@email_marketing.route('/campaign/performance/<int:campaign_id>', methods=['GET'])
@cache.cached(timeout=50, key_prefix=lambda: f'email_campaign_performance_cache_{request.view_args["campaign_id"]}')
@login_required
def email_campaign_performance(campaign_id):
    # Your code to fetch and display the campaign performance for the given campaign_id
    open_rate = campaign_open_rate(campaign_id)
    unique_opens = get_unique_opens(campaign_id)  # This function would get the number of unique opens
    total_opens = market.get_total_opens(campaign_id)

    click_rate = market.get_click_rate(campaign_id)
    unique_clicks = market.get_unique_clicks(campaign_id)
    total_clicks = market.get_total_clicks(campaign_id)

    click_events = {'click_rate': click_rate, 'unique_clicks': unique_clicks, "total_clicks": total_clicks}

    event_metrics = market.get_event_metrics(campaign_id)

    total_emails_sent = market.total_email_list(campaign_id)

    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('per_page', 25, type=int)

    events = market.get_customer_campaign_events(campaign_id, page, items_per_page)
    total_pages = math.ceil(total_emails_sent / items_per_page)

    campaign_subject= get_email_campaign_subject(campaign_id)


    return render_template("campaign_performance.html", events=events, total_emails_sent=total_emails_sent, **event_metrics,
                           click_events=click_events, campaign_id=campaign_id, open_rate=open_rate,
                           unique_opens=unique_opens, total_opens=total_opens,campaign_subject=campaign_subject,page=page,total_pages=total_pages)


@email_marketing.route('/sending-marketing-emails/sending-email-campaign/', methods=['GET', 'POST'])
def send_marketing_emails():
    if request.method == "POST":
        data = request.json
        print(data)
        from_address = data['fromAddress']
        contacts_type = data['customerType']
        email_subject = data['emailSubject']
        email_body = data['emailBody']
        user_id = current_user.id
        recipient_list = get_customers_by_year_or_all(contacts_type)
        # email_list = [('daniel', "mrboadu3@gmail.com"), ('kofi', "kboadu16@gmail.com")]

        campaign_id = marketing_email(

            user_id=user_id,
            total_number_of_email_list=len(recipient_list),
            campaign_subject=email_subject,
            campaign_body=email_body,
            campaign_status="sent"
        )
        try:
            if campaign_id:
                market.enqueue_email_task(recipient_list, email_subject, from_address, email_body, campaign_id)
                performance_url = url_for('marketing.email_campaign_performance',
                                          campaign_id=campaign_id) + "?message=email_processing" + "&campaign_id=" + str(
                    campaign_id)
                return jsonify({"message": "Email tasks queued for sending", "redirectUrl": performance_url})
            else:
                logging.error("Failed to create campaign entry in the database.")
                return jsonify({"error": "Failed to create campaign entry in the database."}), 500
        except Exception as e:
            logging.error(f"Error queuing marketing emails: {e}")
            return jsonify(
                {"error": "An error occurred while queuing marketing emails.", "redirectUrl": "/marketing/emails"}), 500

    else:

        senders = get_all_users()

        customer_list_by_year = our_customers_since_by_year()

        return render_template("send_marketing_email.html", senders=senders, customer_list_byYear=customer_list_by_year)







@email_marketing.route('/campaign/delete/', methods=['POST'])
@login_required
def delete_email_campaign():
    campaign_id = request.form.get('deleting-campaign_id')
    if campaign_id:
        market.delete_campaign(campaign_id)

    return redirect(url_for("marketing.marketing_emails"))
