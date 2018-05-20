from django.contrib import admin
from django.contrib.sessions.models import Session
from . import models

# Register your models here.


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    ordering = ('last_name',)


class BoardAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'day')
    ordering = ('-timestamp',)


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('board', 'order', 'number', 'start_time', 'end_time')
    ordering = ('board', 'order', 'start_time')


class AbsentAdmin(admin.ModelAdmin):
    list_display = ('board', 'teacher')
    ordering = ('board',)


class GraphAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated')


class GraphEntryAdmin(admin.ModelAdmin):
    list_display = ('graph', 'name', 'value', 'color')


class SuperMessageAdmin(admin.ModelAdmin):
    pass




admin.site.register(Session, SessionAdmin)

admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Board, BoardAdmin)
admin.site.register(models.Period, PeriodAdmin)
admin.site.register(models.Absent, AbsentAdmin)

admin.site.register(models.SuperMessage, SuperMessageAdmin)

admin.site.register(models.Graph, GraphAdmin)
admin.site.register(models.GraphEntry, GraphEntryAdmin)


