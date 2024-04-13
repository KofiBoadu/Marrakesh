from . import fileImport_bp
from flask import  render_template, request,redirect,url_for,flash
from werkzeug.utils import secure_filename
import os
from  .import_model   import process_csv

@fileImport_bp.route('/upload', methods=['POST'])
def upload_file():
    # Check if 'file' is present in request.files
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for("contacts.home_page"))

    file = request.files['file']
    # Check if the user did not select a file or the file has an empty name
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for("contacts.home_page"))

    # Securely get the file's name and extension to check its format
    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext != ".csv":
        flash('Wrong file format. Please make sure it’s a CSV file.')
        return redirect(url_for("contacts.home_page"))

    # If the file is present and correct, process the CSV
    print(filename)
    process_csv(file)
    flash('File has been successfully uploaded and processed.')
    return redirect(url_for("contacts.home_page"))

    


