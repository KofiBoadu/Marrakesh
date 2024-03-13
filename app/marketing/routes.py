from flask import  render_template, request,redirect,url_for,flash
from . import email_marketing
from  app.mass_email_marketing import send_emails_asynchronously
from app.user import get_all_users
from app.emails import our_customers_sincebyYear,get_customers_by_year_or_all
from app.mass_email_marketing import marketing_Email,all_email_campaign,campaign_open_rate,get_unique_opens,get_total_opens
from flask_login import login_required, current_user
import app.mass_email_marketing as market
# Then you can use mem.specific_function(), mem.AnotherClass(), etc.


@email_marketing.route('/emails', methods=['GET'])
@login_required
def marketing_emails():
    campaigns= all_email_campaign()

    return render_template("email_marketing.html",campaigns=campaigns)




@email_marketing.route('/campaign/performance/<int:campaign_id>', methods=['GET'])
@login_required
def email_campaign_performance(campaign_id):

    # Your code to fetch and display the campaign performance for the given campaign_id
    open_rate=campaign_open_rate(campaign_id)
    unique_opens = get_unique_opens(campaign_id)  # This function would get the number of unique opens
    total_opens = get_total_opens(campaign_id)

    click_rate = market.get_click_rate(campaign_id)
    unique_clicks = market.get_unique_clicks(campaign_id)
    total_clicks = market.get_total_clicks(campaign_id)

    click_events= {'click_rate':click_rate,'unique_clicks':unique_clicks,"total_clicks":total_clicks}

    event_metrics = market.get_event_metrics(campaign_id)

    total_emails_sent= market.total_email_list(campaign_id)



    # total_bounce=market.get_bounces(campaign_id)
    # total_delivery=market.get_successful_deliveries(campaign_id)
    # total_unsubscribe=market.get_unsubscribes(campaign_id)
    # total_spam=market.get_spam_reports(campaign_id)


    # delivery_events={"total_bounce":total_bounce,"total_delivery":total_delivery,"total_unsubscribe":total_unsubscribe,"total_spam":total_spam}




    return render_template("email_campaign.html",total_emails_sent=total_emails_sent,**event_metrics, click_events=click_events,campaign_id=campaign_id,open_rate=open_rate, unique_opens= unique_opens,total_opens=total_opens)











@email_marketing.route('/sending-emails', methods=['GET', 'POST'])
@login_required
def create_marketingEmails():
    if request.method == 'POST':

        from_address=request.form.get('fromAddress')
        email_subject=request.form.get('emailSubject')
        email_body=request.form.get('emailBody')
        email_list=[("daniel", "mrboadu3@gmail.com"),("abby", "phyllis.kodUA.UAH@gmail.com")]
        user_id=current_user.id
        # d_email_list = email_list * 90


        campaign_id = marketing_Email(
            user_id=user_id,
            total_email_list=len(email_list),
            campaign_subject=email_subject,
            campaign_body=email_body,
            campaign_status="sent"
        )


        if campaign_id:
            # Modify send_emails_asynchronously to pass campaign_id to send_email_marketing
            send_emails_asynchronously(email_list, email_subject, from_address, email_body, campaign_id)
        else:
            print("Failed to create campaign entry in the database.")



        # send_emails_asynchronously(email_list, email_subject, from_address, email_body)
        # # Now, insert campaign details into the database

        return redirect(url_for("marketing.marketing_emails"))

    senders = get_all_users()
    customer_list_byYear = our_customers_sincebyYear()
    return render_template("sendEmail_marketing.html", senders=senders, customer_list_byYear=customer_list_byYear)




