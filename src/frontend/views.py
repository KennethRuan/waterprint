from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from datetime import date, datetime, timedelta
from django.forms.utils import ErrorList

from .forms import CreateUserForm, WaterUsageForm, AddFriendsForm

# Create your views here.
@login_required(login_url="login")
def home_view(request):
    # static variables
    num_of_weeks = 8 # num of weeks to display for history

    profile = Profile.objects.filter(person_of=request.user).last()

    #creating a new profile for each day
    if date.today() > profile.date:
        profile=Profile.objects.create(person_of=request.user)
        profile.save()

    profile = Profile.objects.filter(person_of=request.user).last()

    profiles = Profile.objects.filter(person_of=request.user).order_by("-id")
    current_year = profile.date.isocalendar()[0]
    current_week = profile.date.isocalendar()[1]
    week_data = [i.date.isocalendar()[1] for i in profiles]
    week_data = [[current_week-num_of_weeks+i+1, 0.0] for i in range(num_of_weeks)]

    for x in profiles:
        year_number = x.date.isocalendar()[0]
        week_number = x.date.isocalendar()[1]
        year_diff = current_year - year_number
        week_diff = current_week - week_number
        if year_diff > 0 or week_diff >= num_of_weeks:
            break
        
        week_data[num_of_weeks-week_diff-1][1] += x.water_usage

    print(week_data)
    water_usage = profile.water_usage

    friends = profile.friends_list
    friends_form = AddFriendsForm()
    if request.method == "POST":
        form = AddFriendsForm(request.POST)
        if form.is_valid():
            friend_name = request.POST.get("username")
            friend_object = User.objects.get(username=friend_name)

            friended_user_profile = Profile.objects.filter(person_of=friend_object).last()
            print(friended_user_profile)
            if friended_user_profile is not None:
                print("Succesfully added: " + friend_name)
                profile.add_friend(friended_user_profile)
            else:
                print("Error")
                errors = form._errors.setdefault("username", ErrorList())
                errors.append(u"The User that was Entered is Invalid")
        else:
            print(form.errors)
    

    context = {"water_usage":water_usage, "week_data":week_data, "friends_form":friends_form}
    return render(request, 'frontend/home.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CreateUserForm()
    form_errors = {}

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Account Created for " + username)
            Profile.objects.filter(person_of=username).relations.clear() # clears all m2m relationships

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


