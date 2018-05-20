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


# ## SUPER MESSAGE ## #

# A message that appears at the very top and bypasses any implemented Gauth and is
# not archived. Only one should exist at a time
class SuperMessage(models.Model):
    heading = models.TextField(null=True)
    message = models.TextField(null=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.updated)


# ## GRAPH ## #

# A graph to show progress between groups; ex: spirit week
# This is not archived and only one should exist at a time
class Graph(models.Model):
    title = models.TextField(null=True)
    updated = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.title)


class GraphEntry(models.Model):
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    name = models.TextField(null=True)
    value = models.FloatField(default=0)
    color = models.TextField(null=True)

    def __str__(self):
        return str(self.name) + " " + str(self.graph)


# ## BOARD ## #


# Data about a teacher, only for autocomplete and lookup
class Teacher(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def formatted(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.last_name + ', ' + self.first_name


# Data for a board entry
class Board(models.Model):
    timestamp = models.DateTimeField(default=now)
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
        return str(self.timestamp.date())


# Data for period times on the board
# NOT the periods teachers are out.
class Period(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    number = models.CharField(max_length=50)
    start_time = models.CharField(max_length=150)
    end_time = models.CharField(max_length=150)

    def __str__(self):
        return str(self.board.timestamp.date())


# Data for a teacher absent on the board.
class Absent(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=200)
    hours = models.CharField(max_length=150)

    def __str__(self):
        return self.teacher + ' ' + self.hours

