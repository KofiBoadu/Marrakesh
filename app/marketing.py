# from mailchimp_marketing import Client
# import os
# from dotenv import load_dotenv
# import mailchimp_marketing as MailchimpMarketing
# from mailchimp_marketing.api_client import ApiClientError


# load_dotenv()





# client = MailchimpMarketing.Client()
# client.set_config({
#   "api_key": os.getenv('MAIL_CHIMP'),
#   "server": os.getenv('MAIL_CHIMP_SERVERPREFIX')
# })

# response = client.ping.get()
# print(response)





# list_id = "0ef98e1461"

# member_info = {
#     "email_address": "mrboadu3@gmail.com",
#     "status": "subscribed",
#     "merge_fields": {
#       "FNAME": "Daniel",
#       "LNAME": "Boadu"
#     }
#   }


# try:
#   response = client.lists.add_list_member(list_id, member_info)
#   print("response: {}".format(response))
# except ApiClientError as error:
#   print("An exception occurred: {}".format(error.text))













