from flask_login import login_required,current_user
from app.user  import get_user,User
from . import fileExport_bp
from flask import  render_template, request,redirect,url_for,flash,session
from app.exporting_file import export_customer_data,export_data,make_file_public,get_download_link,upload_file,send_file_email



@fileExport_bp.route('/export', methods=['POST'])
@login_required
def export_file():
	customers= export_customer_data()
	filename= export_data(customers, 'csv')
	filepath='/Users/danielkofiboadu/Desktop/Travel-Torch-CRM/'+filename

	file=upload_file(filename, filepath, 'text/'+'csv')

	make_file_public(file)

	download=get_download_link(file)
	login_user=current_user
	sender="bookings@africatravellers.com"
	reciever_user_email=login_user.email_address
	subject = "exported file ready"
	recipients= [reciever_user_email]
	text_body = "Click to download the requested data"
	html_body = f"""
	<h1>This is the HTML Body of the Email</h1>
	<p>This part is in <strong>bold</strong>.</p>
	<p>Visit <a href='{download}'</a> for more information.</p>
	"""

	send_file_email(subject, sender, recipients, text_body, html_body)


	return redirect(url_for("customers.home_page"))






