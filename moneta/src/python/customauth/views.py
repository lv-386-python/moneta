from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserLoginForm


@login_required
def home(request):
    return render(request, 'home.html')


def login_view(request):
    # if not request.user.is_authenticated:
    #     return redirect("/")
    next = request.GET.get('next')
    form = UserLoginForm(request.POST)
    print(form.is_valid())

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            return redirect('moneta-home')

    print("test")
    context = {'form': form}
    return render(request, "login_app/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('customauth')
