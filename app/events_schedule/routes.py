from .import events
from flask import  render_template, request,redirect,url_for,flash
from app.events import all_scheduled_events











@events.route('/upcoming_events', methods=['GET'])
def events_home():
    upcoming_events = all_scheduled_events()
    first_event = upcoming_events[0] if upcoming_events else None
    print(first_event)
    return render_template("events.html", event=first_event)

