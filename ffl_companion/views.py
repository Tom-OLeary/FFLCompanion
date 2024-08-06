import posixpath
from pathlib import Path

from django import forms
from django.contrib.auth.hashers import check_password
from django.utils._os import safe_join
from django.views.static import serve as static_serve
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ffl_companion.api_models.owner import TeamOwner
from ffl_companion.config import App
from ffl_companion.serializers import LoginSerializer


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


class AppLoginView(GenericAPIView):
    queryset = TeamOwner.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        try:
            App.unlock()
            owner = TeamOwner.objects.get(name=user)
            App.lock()
        except TeamOwner.DoesNotExist:
            App.lock()
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, owner.password):
            login(request, owner)
            try:
                initiate_app(owner)
            except AttributeError:
                return Response({"error": "User League Not Found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        return Response("ok", status=status.HTTP_200_OK)


# TODO implement
def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')


def initiate_app(owner: TeamOwner):
    """Sets global database filter for this owner's league"""
    App.lock()
    App.set(owner.league_name)
