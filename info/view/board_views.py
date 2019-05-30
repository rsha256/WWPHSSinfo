from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from info import models
from info.handlers import board_handler


@login_required
def post_board(request):

    if request.method == "POST":

        post_dict = dict(request.POST)

        message_only = True if request.POST.get('message_type') is not None else False

        if not message_only:

            day = request.POST.get('day')
            announcements = request.POST.get('announcements')
            quote = request.POST.get('quote')
            schedule = []
            absents = []

            # Schedule
            if request.POST.get("periodNames[]"):
                numbers = post_dict["periodNames[]"]
                starts = post_dict["periodStarts[]"]
                ends = post_dict["periodEnds[]"]

                for i in range(0, len(numbers)):
                    if numbers[i] is not '':
                        schedule.append({"order": i, "name": numbers[i], "start": starts[i], "end": ends[i]})

            # Absent Teachers
            if request.POST.get("teacherNames[]"):
                names = post_dict["teacherNames[]"]
                hours = post_dict["teacherHours[]"]

                for i in range(0, len(names)):
                    if names[i] is not '':
                        absents.append({'teacher': names[i], 'hours': hours[i]})

            data = {
                'message_only': False,
                'day': day,
                'announcements': announcements,
                'quote': quote,
                'schedule': schedule,
                'absents': absents
            }

        else:
            data = {
                'message_only': True,
                'message': request.POST.get('message')
            }

        board_handler.handle(data)

    return render(request, 'info/board/postBoard.html', {
        'data': board_handler.get_today(),
        'teachers': models.Teacher.objects.all(),
    })


@login_required
def archive(request, date=None):

    if date is None:
        return render(request, 'info/board/archive.html', {
            'all_dates': models.Board.objects.order_by('-timestamp').values('timestamp')
        })

    try:
        data = board_handler.get_date(date)
    except:
        raise Http404("Board does not exist")

    return render(request, 'info/board/archive.html', {
        'data': data,
        'previous': None,
        'next': None,
        'suppress_outdated_warning': True,
    })
