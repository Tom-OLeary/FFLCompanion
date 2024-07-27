import posixpath
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.utils._os import safe_join
from django.views.static import serve as static_serve
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from ffl_companion.api_models.owner import TeamOwner
from ffl_companion.config import App


# @login_required(login_url='login')
def serve_react(request, html_path, document_root=None):
    path = posixpath.normpath(html_path).lstrip("/")
    fullpath = Path(safe_join(document_root, path))
    if fullpath.is_file():
        return static_serve(request, path, document_root, show_indexes=True)
    else:
        return static_serve(request, "index.html", document_root, show_indexes=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home/')

        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user = authenticate(request, username=username, password=password)
            # print("kkkkkkkkkkkkk", request)
            # if user is not None:
            try:
                owner = TeamOwner.objects.get(name=username)
            except TeamOwner.DoesNotExist:
                messages.error(request, f'User not found')
                return render(request, 'login.html', {'form': form})

            if check_password(password, owner.password):
                login(request, owner)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                try:
                    initiate_app(owner)
                except AttributeError:
                    messages.error(request, f'User League Not Found')
                    return render(request, 'login.html', {'form': form})

                return redirect('home/')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')


def initiate_app(owner: TeamOwner):
    App.set("LeagueSettingsManager", owner.get_league_settings())
