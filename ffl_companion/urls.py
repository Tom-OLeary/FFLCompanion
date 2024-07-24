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

# from homepage import views as homepage_views
from ffl_companion.views import serve_react

django_app_patterns = [
    path('admin/', admin.site.urls),
    # path('', homepage_views.home_index, name="homepage"),
    # path("projects/", include("projects.urls")),
    # path("resume/", include("resume.urls")),
    path("api/", include("api.urls")),
]
react_patterns = [
    path("", serve_react, {"document_root": settings.REACT_FANTASY_TRACKER_BUILD_PATH, "html_path": ""}),
    # path("home/", serve_react, {"document_root": settings.REACT_FANTASY_TRACKER_BUILD_PATH, "html_path": ""}),
]

urlpatterns = [
    *django_app_patterns,
    *react_patterns,
]

