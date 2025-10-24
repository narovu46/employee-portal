from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/",  auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", dashboard, name="dashboard"),  # dashboard at root
]
