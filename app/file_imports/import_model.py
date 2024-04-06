from app.models import add_new_contact,check_contact_exists





def process_csv(file):
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)
    for row in csv_input:
        email = row['Email'].strip().lower()
        # Check if the contact already exists
        if not check_contact_exists(email):
            # Add new contact
            add_new_contact(
                first_name=row['First Name'].strip(),
                last_name=row['Last Name'].strip(),
                email=email,
                phone=row.get('Phone', None),
                gender=row.get('Gender', None),
                state=row.get('State', None),
                lead_status=row.get('Lead Status', 'Lead')
            )



