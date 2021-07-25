from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

@login_required(login_url="login")
def friends_view(request):
    profile = Profile.objects.filter(person_of=request.user).last()
    profile_follows = ProfileFollowing.objects.filter(follower=profile)
    followed_profiles = []
    for p in profile_follows:
        fp = p.followed
        followed_profiles.append([fp.total_usage, fp.person_of.username]) # name and total usage over competition time
    followed_profiles.append([profile.total_usage, profile.person_of.username])
    followed_profiles = sorted(followed_profiles)
    print(followed_profiles)
    return render(request,"friends.html", {"followed_profiles": followed_profiles})