from django.shortcuts import render

from django.utils import timezone
from .models import Event


def countdown_timer(request):
    event = Event.objects.first()
    if event:
        time_remaining = event.event_date - timezone.now()
        hours = time_remaining.seconds
        minutes = time_remaining.seconds
        seconds = time_remaining.seconds
        data = {
            'name': event.name,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }
    else:
        data = {
            'name': "No Event",
            'hours': 0,
            'minutes': 0,
            'seconds': 0
        }
    return render(request, 'myapp.html', {'data': data})
