import posixpath
from pathlib import Path

from django import forms
from django.contrib.auth.hashers import check_password, make_password
from django.utils._os import safe_join
from django.views.static import serve as static_serve
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect

from api.api_util import BaseAPIView
from ffl_companion.serializers import LoginSerializer, PasswordSerializer
from owner.models import Owner


def serve_react(request, html_path, document_root=None):
    path = posixpath.normpath(html_path).lstrip("/")
    fullpath = Path(safe_join(document_root, path))
    if fullpath.is_file():
        return static_serve(request, path, document_root, show_indexes=True)
    else:
        return static_serve(request, "index.html", document_root, show_indexes=True)


def redirect_to_home(request):
    return HttpResponseRedirect("/")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class AppLoginView(GenericAPIView):
    queryset = Owner.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        try:
            owner = Owner.objects.get(username=user)
        except Owner.DoesNotExist:
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, owner.password):
            login(request, owner)
            token, created = Token.objects.get_or_create(user=owner)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Incorrect Password"}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(BaseAPIView):
    model = Owner

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(self.AUTHENTICATION_MSG, status=status.HTTP_401_UNAUTHORIZED)

        dataset = request.user.__dict__.get("dataset")
        if dataset is None or dataset == "Demo":
            return Response("Demo User Cannot Change Password", status=status.HTTP_401_UNAUTHORIZED)

        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if check_password(serializer.validated_data["current_password"], request.user.password):
            request.user.set_password(serializer.validated_data["new_password"])
            return Response("ok", status=status.HTTP_200_OK)
        else:
            return Response("Incorrect Password", status=status.HTTP_400_BAD_REQUEST)


# TODO implement
def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')

