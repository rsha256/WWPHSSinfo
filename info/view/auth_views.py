from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user


def login(request):
    if request.user.is_authenticated:
        return redirect("/staff")

    if request.method == 'POST':
        username = request.POST['username'].lower().strip()
        password = request.POST['password'].strip()

        user = authenticate(username=username, password=password)

        if user is not None:
            login_user(request, user)

            if request.GET.get('next') is not None:
                return redirect(request.GET['next'])
            return redirect('/staff')

        else:
            return render(request, 'info/staff/login.html', {
                "continue": request.GET.get('next'),
                'error': 'invalid',
            })

    return render(request, 'info/staff/login.html', {"continue": request.GET.get('next')})


@login_required
def logout(request):
    logout_user(request)
    return redirect('/login')

