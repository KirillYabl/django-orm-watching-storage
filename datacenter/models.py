from django.db import models
from django.utils.timezone import localtime

import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        now = get_local_now()
        leaved_at = self.leaved_at or now
        return (leaved_at - localtime(self.entered_at))

    def is_visit_long(self, minutes=60):
        visit_duration = self.get_duration()
        total_minutes = visit_duration.total_seconds() / 60

        visit_more_then_minutes = total_minutes > minutes        
        return visit_more_then_minutes



def format_duration(duration):
    seconds = duration.total_seconds()
    days = duration.days
    last_day_seconds = duration.seconds
    hours = int(last_day_seconds // 3600)
    minutes = int((last_day_seconds % 3600) // 60)

    return f'{days}сут {hours}ч {minutes}мин'

def get_local_now(seconds=10800):
      tzinfo=datetime.timezone(datetime.timedelta(seconds=seconds))
      now = datetime.datetime.now().replace(tzinfo=tzinfo)

      return now

