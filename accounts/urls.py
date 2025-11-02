from django.urls import path
from .views import UserLoginView, user_logout, dashboard, autologin, home

urlpatterns = [

    path("", home, name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("auto-login/", autologin, name="auto_login"),
]
