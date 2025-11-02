import time, hmac, hashlib
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")

class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm(request)
        return render(request, "login.html", {"form": form})
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        return render(request, "login.html", {"form": form, "error": "Invalid credentials"})

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"username": request.user.username})

def autologin(request):
    u  = request.GET.get("u")
    ts = request.GET.get("ts")
    sig = request.GET.get("sig", "").lower()
    if not (u and ts and sig):
        return HttpResponseBadRequest("missing parameters")
    try:
        ts = int(ts)
    except ValueError:
        return HttpResponseBadRequest("bad timestamp")

    now = int(time.time())
    window = 600 if settings.DEBUG else 120
    if abs(now - ts) > window:
        return HttpResponseBadRequest("expired")

    payload = f"{u}|{ts}".encode("utf-8")
    key = settings.AUTOLOGIN_SHARED_SECRET.encode("utf-8")
    expect = hmac.new(key, payload, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expect, sig):
        return HttpResponseBadRequest("bad signature")

    user, _ = User.objects.get_or_create(username=u, defaults={"is_active": True})
    user.set_unusable_password(); user.save()
    login(request, user)
    return redirect("dashboard")
