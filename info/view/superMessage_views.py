from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from info import models


@login_required
def super_message_post(request):
    if request.method == "POST":
        msg = models.SuperMessage()
        msg.heading = request.POST['heading']
        msg.message = request.POST['message']
        msg.save()

    return redirect("/staff")


@login_required
def super_message_delete(request):
    if request.method == "POST":
        models.SuperMessage.objects.all().delete()

    return redirect("/staff")


def super_message_get():
    super_msg = models.SuperMessage.objects.all()
    if super_msg:
        super_msg = super_msg[0]
    return super_msg

