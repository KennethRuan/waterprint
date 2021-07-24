from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from datetime import date, datetime, timedelta

from .forms import CreateUserForm, WaterUsageForm, AddFriendsForm

@login_required(login_url="login")
def water_usage_view(request):
    person = Profile.objects.filter(person_of=request.user).last()
    form = WaterUsageForm(instance=person)

    if request.method == "POST":
        form = WaterUsageForm(request.POST, instance=person)
        if form.is_valid():
            profile = form.save()
            profile.save()
            return redirect("home")

    context = {"form":form}
    return render(request,"frontend/water_usage.html", context)