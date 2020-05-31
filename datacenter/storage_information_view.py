from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render
from django.utils.timezone import localtime

import datetime


def storage_information_view(request):
    not_leaved_visits = Visit.objects.filter(leaved_at=None).all()

    non_closed_visits = [
        {
            "who_entered": visit.passcard.owner_name,
            "entered_at": localtime(visit.entered_at),
            "duration": format_duration(visit.get_duration()),
            "is_strange": visit.is_visit_long()
        }
        for visit in not_leaved_visits
    ]
    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
