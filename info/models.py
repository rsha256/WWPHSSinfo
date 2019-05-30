from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from WWPHSSinfo.settings import PRODUCTION

# Load User model based on environment
if PRODUCTION:
    from djangae.contrib.gauth_datastore.models import GaeDatastoreUser

    User = GaeDatastoreUser
else:
    from django.contrib.auth.models import User


# Create your models here.

####################
#    ACTIVITIES    #
####################

class Sport(models.Model):
    """
    A Single Sport for display on activities page
    """

    GENDERS = (
        ('B', 'Boys'),
        ('G', 'Girls'),
    )

    SEASONS = (
        ('F', 'Fall'),
        ('W', 'Winter'),
        ('S', 'Spring'),
    )

    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=8, choices=GENDERS, default=None, null=True)
    season = models.CharField(max_length=10, choices=SEASONS, default=None, null=True)
    coach = models.TextField(null=True)

    def __str__(self):
        return self.gender + ' ' + self.name


class Club(models.Model):
    """
    A Single club for display on activities page
    """

    MEETING_DAYS = (
        ('M', 'Monday'),
        ('Tu', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, default=None)
    meeting_day = models.CharField(max_length=10, choices=MEETING_DAYS, default=None, null=True)
    location = models.CharField(max_length=25, null=True)
    adviser = models.TextField(null=True, default=None)
    email = models.EmailField(null=True, default=None)

    def __str__(self):
        return self.name


#######################
#    SUPER MESSAGE    #
#######################


class SuperMessage(models.Model):
    """
     A message that appears at the very top and bypasses any implemented Gauth and is
     not archived. Only one should exist at a time
    """

    heading = models.TextField(null=True)
    message = models.TextField(null=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.updated)


###############
#    GRAPH    #
###############


class Graph(models.Model):
    """
    A graph to show progress between groups; ex: spirit week
    This is not archived and only one should exist at a time
    """

    title = models.TextField(null=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.title)


class GraphEntry(models.Model):
    """
    A Single entry
    key, value data
    """

    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    name = models.TextField(null=True)
    value = models.FloatField(default=0)
    color = models.TextField(null=True)

    def __str__(self):
        return str(self.name) + " " + str(self.graph)


###############
#    BOARD    #
###############


class Teacher(models.Model):
    """
    Data about a teacher, only for autocomplete and lookup
    """

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def formatted(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.last_name + ', ' + self.first_name


class Board(models.Model):
    """
    Data for a board entry
    """

    timestamp = models.DateField()
    announcements = models.TextField(null=True)
    quote = models.TextField(null=True)

    message_only = models.BooleanField(default=False)
    message = models.TextField(default=None, null=True)

    DAY_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('Z', 'Zero'),
    )

    day = models.CharField(max_length=5, choices=DAY_CHOICES, default=None, null=True)

    def __str__(self):
        return str(self.timestamp)


class Period(models.Model):
    """
    Data for period times on the board
    NOT the periods teachers are out.
    """

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    number = models.CharField(max_length=50)
    start_time = models.CharField(max_length=150)
    end_time = models.CharField(max_length=150)

    def __str__(self):
        return str(self.board.timestamp)


class Absent(models.Model):
    """
    Data for a teacher absent on the board.
    """

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=200)
    hours = models.CharField(max_length=150)

    def __str__(self):
        return self.teacher + ' ' + self.hours
