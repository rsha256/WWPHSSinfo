import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from info import models
from info.view.superMessage_views import *
from info.view.graph_views import *


@login_required
def staff_index(request):

    return render(request, 'info/staff/staffIndex.html', {
        "super_message": super_message_get(),
        "graph_data": graph_get(),
    })


@login_required
def database_update(request):
    if request.method == "POST":
        models.Teacher.objects.all().delete()
        models.Board.objects.all().delete()
        models.SuperMessage.objects.all().delete()
        models.Sport.objects.all().delete()
        models.Club.objects.all().delete()

        try:
            file = json.loads((request.FILES['data'].read()).decode("utf-8", "strict"))

            for t in file['teachers']:
                teacher = models.Teacher()
                teacher.first_name = t['first']
                teacher.last_name = t['last']
                teacher.save()

            for s in file['sports']:
                sport = models.Sport()
                sport.name = s['name']
                sport.gender = s['gender']
                sport.season = s['season']
                sport.coach = s['coach']
                sport.save()

            for c in file['clubs']:
                club = models.Club()
                club.name = c['name']
                club.description = c['description']
                club.meeting_day = c['meeting_day']
                club.location = c['location']
                club.adviser = c['adviser']
                club.email = c['email']
                club.save()

            success = True

        except Exception:
            success = False

        return render(request, 'info/staff/databaseUpdate.html', {'success': success})

    return render(request, 'info/staff/databaseUpdate.html', {})
