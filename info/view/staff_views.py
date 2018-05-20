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

        try:
            file = json.loads((request.FILES['teachers'].read()).decode("utf-8", "strict"))
            for t in file:
                teacher = models.Teacher()
                teacher.first_name = t['first']
                teacher.last_name = t['last']
                teacher.save()

            success = True

        except Exception:
            success = False

        return render(request, 'info/staff/databaseUpdate.html', {'success': success})

    return render(request, 'info/staff/databaseUpdate.html', {})
