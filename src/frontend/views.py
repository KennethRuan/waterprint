from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from datetime import date, datetime, timedelta

from .forms import CreateUserForm, WaterUsageForm

# Create your views here.
@login_required(login_url="login")
def home_view(request):

    #creating a new profile for each day
    if date.today() > watertracker.date:
        profile=Profile.objects.create(person_of=request.user)
        profile.save()

    profile = Profile.objects.filter(person_of=request.user).last()
    water_usage = profile.water_usage
    context = {"water_usage":water_usage}
    return render(request, 'frontend/home.html', context)

@login_required(login_url="login")
def water_usage_view(request):
    form = WaterUsageForm()
    if request.method == "POST":
        form = WaterUsageForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.person_of = request.user
            profile.save()
            return redirect("home")

    context = {"form":form}
    return render(request,"frontend/water_usage.html", context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created for " + form.cleaned_data.get("username"))

            return redirect('login')

    context = {"form": form}
    return render(request, 'frontend/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is Invalid')

    context = {}
    return render(request, 'frontend/login.html', context)

def logout_view(request):
    logout(request)
    return redirect("login")


