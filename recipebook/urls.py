"""
URL configuration for recipebook project.

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

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),  # URL for the home view
    path("recipes/", include("recipes.urls")),  # Include the recipes app URLs
    path(
        "login/", auth_views.LoginView.as_view(), name="login"
    ),  # URL for the login view
    path(
        "logout/", auth_views.LogoutView.as_view(), name="logout"
    ),  # URL for the logout view
    path("signup/", views.signup_view, name="signup"),  # URL for the signup view
    path(
        "login-required/", views.login_required_message, name="login_required_message"
    ),  # URL for login required message
]
