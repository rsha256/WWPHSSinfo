from django.utils import timezone
from datetime import date
from dateutil import parser as date_parser
from info import models


def get_date(date):
    date = date_parser.parse(date)
    board = models.Board.objects.filter(timestamp__date=date)[0]
    schedule = models.Period.objects.filter(board=board).order_by('order')
    absents = models.Absent.objects.filter(board=board)

    return {
        'board': board,
        'schedule': schedule,
        'absents': absents
    }


def get_today():
    try:
        return get_date(str(date.today()))
    except IndexError:
        return None


def get_latest():

    # throws IndexError if no boards exist
    latest_date = models.Board.objects.order_by('-timestamp')[0].timestamp
    return get_date(str(latest_date))


def today_exists():
    board = models.Board.objects.filter(timestamp__date=date.today())
    return board.exists()


def handle(data):
    if today_exists():
        __update_current(data)
    else:
        __post_new(data)


def __update_current(data):
    board = models.Board.objects.filter(timestamp__date=date.today())
    board.delete()
    __post_new(data)


def __post_new(data):
    board = models.Board()

    if not data['message_only']:
        board.timestamp = timezone.now()
        board.message_only = False
        board.day = data['day']
        board.announcements = data['announcements']
        board.quote = data['quote']
        board.save()

        # schedule
        for period in data['schedule']:
            slot = models.Period()
            slot.board = board
            slot.order = period['order']
            slot.number = period['name']
            slot.start_time = period['start']
            slot.end_time = period['end']
            slot.save()

        # Absent Teachers
        for teacher in data['absents']:
            absent = models.Absent()
            absent.board = board
            absent.teacher = teacher['teacher']
            absent.hours = teacher['hours']
            absent.save()
    else:
        board.message_only = True
        board.message = data['message']
        board.save()


def to_dict(raw):
    """
   Inputs raw data from the database and transforms it into a universally structure.
   It uses Django models imports; therefore restricted.
   Useful for serialization.

   :param raw: data from database, in form of queryset
   :return: universal dictionary
   """
    return {
        'board': {
            'timestamp': str(raw['board'].timestamp),
            'day': raw['board'].day,
            'message_only': raw['board'].message_only,
            'message': raw['board'].message,
            'announcements': raw['board'].announcements,
            'quote': raw['board'].quote,
        },

        'schedule': [
            {
                "number": i.number,
                "start": i.start_time,
                "end": i.end_time
            }
            for i in raw['schedule']],

        'absents': [
            {
                "teacher": i.teacher,
                "hours": i.hours
            }
            for i in raw['absents']
        ],
    }

