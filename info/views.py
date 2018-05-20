"""

Root info views.
Imports other view files.

"""

from django.views.decorators.csrf import ensure_csrf_cookie

from WWPHSSinfo import settings

from info.handlers import gauth_handler

from info.view.auth_views import *
from info.view.board_views import *
from info.view.staff_views import *
from info.view.superMessage_views import *
from info.view.graph_views import *

# Create your views here.


@ensure_csrf_cookie
def index(request):

    # board
    try:
        data = board_handler.get_latest()
    except IndexError:
        data = "NoneToShow"

    # super message
    super_msg = super_message_get()

    # Graph
    graph_data = graph_get()

    # Google Auth
    auth = request.user.is_authenticated()

    if request.session.get('gauth') is True:
        auth = True

    if request.method == "POST":
        g_val = gauth_handler.authenticate(request.POST.get('idtoken'))
        if g_val:
            request.session['gauth'] = g_val
            return HttpResponse('{"auth": "OK"}')

    # Render
    return render(request, 'info/index.html', {
        'gauth_key': settings.GAUTH_KEY,
        'auth': auth,
        'data': data,
        "super_message": super_msg,
        "graph_data": graph_data,
    })


def createsuperuser(request):
    '''
    Creates a superuser only if it does not exist already.
    Should be used on new production environments for easy access to the admin panel
    Redirect to login if successful, else redirect to index
    '''

    user = models.User()
    user.username = 'admin'  # change later
    user.email = 'admin@email.com'
    user.set_password("qazwsxed")
    user.is_staff = True
    user.is_superuser = True

    if models.User.objects.filter(username=user.username).exists():
        return redirect('/')
    else:
        user.save()
        return redirect('/staff')

