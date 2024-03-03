from .import events
from flask import  render_template, request,redirect,url_for,flash
from app.events import all_scheduled_events
from flask_login import login_required










@events.route('/upcoming_events', methods=['GET'])
@login_required
def events_home():
    upcoming_events = all_scheduled_events()
    first_event = upcoming_events[0] if upcoming_events else None
    return render_template("events.html", event=first_event)

