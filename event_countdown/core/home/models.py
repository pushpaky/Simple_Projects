from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)  # Event name
    event_date = models.DateTimeField()  # Date and time of the event

    def __str__(self):
        return self.name
