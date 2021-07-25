from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from datetime import date, datetime, timedelta
from django.forms.utils import ErrorList

from .forms import CreateUserForm, WaterUsageForm, AddFriendsForm

# Create your views here.
@login_required(login_url="login")
def home_view(request):
    # static variables
    num_of_weeks = 8 # num of weeks to display for history
    competition_duration = 4 # num of weeks to display for leaderboard

    # resetting session variable
    request.session["new_food_list"] = True
    request.session["search_occured"] = False

    profile = Profile.objects.filter(person_of=request.user).last()

    # creating a new profile for each day
    if date.today() > profile.date:
        profile=Profile.objects.create(person_of=request.user)
        profile.save()

    profile = Profile.objects.filter(person_of=request.user).last()

    # gathering chart data using existing profiles
    profiles = Profile.objects.filter(person_of=request.user).order_by("-id")
    current_year = profile.date.isocalendar()[0]
    current_week = profile.date.isocalendar()[1]
    week_data = [[current_week-num_of_weeks+i+1, 0.0] for i in range(num_of_weeks)]

    profile.total_usage = 0
    for x in profiles:
        year_number = x.date.isocalendar()[0]
        week_number = x.date.isocalendar()[1]
        year_diff = abs(current_year - year_number)
        week_diff = abs(current_week - week_number)
        if (week_diff >= num_of_weeks and week_diff >= competition_duration):
            break
        if (week_diff < num_of_weeks):
            week_data[num_of_weeks-week_diff-1][1] += x.water_usage
        if (week_diff < competition_duration):
            profile.total_usage += x.water_usage
    profile.save()

    print(week_data)
    water_usage = profile.water_usage

    # Adding Friends Component
    friends_form = AddFriendsForm()
    if request.method == "POST":
        friends_form = AddFriendsForm(request.POST)
        if friends_form.is_valid():
            friend_name = request.POST.get("username")

            if User.objects.filter(username=friend_name).exists():
                friend_user = User.objects.get(username=friend_name)
                friend_profile = Profile.objects.filter(person_of=friend_user).last()
                user_profile = profile
                print("Succesfully added: " + friend_name)
                if not ProfileFollowing.objects.filter(Q(follower=user_profile) & Q(followed=friend_profile)).exists():
                    ProfileFollowing.objects.create(follower=user_profile, followed=friend_profile)
                else:
                    print("Error: Already Following")
                    errors = friends_form.add_error("username", "Already following that user")
            else:
                print("Error: Invalid User")
                errors = friends_form.add_error("username", "The user that was entered is invalid")
        else:
            print(friends_form.errors)

    # Gathering leaderboard from following
    profile_follows = ProfileFollowing.objects.filter(follower=profile)
    followed_profiles = []
    for p in profile_follows:
        fp = p.followed
        followed_profiles.append([fp.total_usage, fp.person_of.username]) # name and total usage over competition time
    followed_profiles.append([profile.total_usage, profile.person_of.username])
    followed_profiles = sorted(followed_profiles)
    
    # compiling indices to display
    lb_ind = [0]
    
    user_ind = 0
    for i,x in enumerate(followed_profiles):
        if x[1] == profile.person_of.username:
            user_ind = i
            break
    
    #percentile calculation
    users_below = (len(followed_profiles)-user_ind-1)
    total_other_users = (len(followed_profiles)-1)
    if total_other_users == 0:
        percentile = 100
    else:
        percentile = int(round(users_below/total_other_users))

    #leaderboard display calculation
    if user_ind not in lb_ind:
        lb_ind.append(user_ind)
    
    if (user_ind - 1) >= 0 and (user_ind - 1) not in lb_ind:
        lb_ind.append(user_ind-1)
    
    if (user_ind + 1) < len(followed_profiles) and (user_ind + 1) not in lb_ind:
        lb_ind.append(user_ind+1)

    if (len(followed_profiles)-1) not in lb_ind:
        lb_ind.append(len(followed_profiles)-1)

    lb_ind=sorted(lb_ind)
    lb_display = [followed_profiles[i] for i in lb_ind]
    
    print(lb_display)

    daily_usage = Profile.objects.filter(person_of=request.user).last().water_usage

    last_entry_object = FoodList.objects.filter(user=request.user).last()
    print(last_entry_object)
    last_food_list = FoodItem.objects.filter(food_list=last_entry_object)
    last_entry = []
    last_water_usage = 0
    for obj in last_food_list:
        # print(obj.food, obj.footprint)
        last_entry.append([obj.food, obj.footprint])
        last_water_usage += obj.footprint

    last_water_usage_str = ""
    if last_food_list.exists():
        last_water_usage_str = str(last_water_usage) + " L"
    else:
        last_water_usage_str = "N/A"

    # All the processed variables passed into the context
    context = {
        "water_usage":water_usage, 
        "week_data":week_data, 
        "friends_form":friends_form,
        "username": request.user.username,
        "monthly_usage": profile.total_usage,
        "last_usage": last_water_usage_str,
        "percentile": percentile,
        "condensed_leaderboard": lb_display,
        "last_list": last_entry,
        }
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
            # profile = User.objects.get(username=username)
            # user = Profile.objects.filter(person_of=profile).last()

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


