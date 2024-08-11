"""
URL configuration for ffl_companion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from ffl_companion import views
from ffl_companion.views import serve_react, AppLoginView, ChangePasswordView

django_app_patterns = [
    path('admin/', admin.site.urls, name='admin'),
    path("api/", include("api.urls")),
]
react_patterns = [
    path("", serve_react, {"document_root": settings.REACT_FANTASY_TRACKER_BUILD_PATH, "html_path": ""}),
]

login_patterns = [
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout/', views.sign_out, name='logout'),  # TODO not implemented fully
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

urlpatterns = [
    *django_app_patterns,
    *react_patterns,
    *login_patterns,
]

