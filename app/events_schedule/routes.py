from . import events
from flask import render_template
from .scheduled_events import all_scheduled_events
from flask_login import login_required
from app.utils.main import cache


@events.route('/upcoming_events', methods=['GET'])
@login_required
@cache.cached(timeout=5 * 60, key_prefix='events_home')
def events_home():
    upcoming_events = all_scheduled_events()
    first_event = upcoming_events[0] if upcoming_events else None
    return render_template("events.html", event=first_event)
