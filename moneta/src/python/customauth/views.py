from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login, logout)
from .forms import UserLoginForm

incomes = [
    {
        'title': 'SS',
        'currency': 'USD',

    },
    {
        'title': 'LNU',
        'currency': 'UAH',
    }
]


@login_required
def home(request):
    content = {
        'incomes': incomes,
    }
    return render(request, 'www/templates/sidebar.html', content)


def login_view(request):
    # if not request.user.is_authenticated:
    #     return redirect("/")
    next = request.GET.get('next')
    form = UserLoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('moneta-home')


    context = {'form': form}
    return render(request, "customauth.html", context)


def logout_view(request):
    logout(request)
    return redirect('customauth')
