from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from datetime import date, datetime, timedelta
from watertracker.wsgi import *
from .forms import CreateUserForm, WaterUsageForm, AddFriendsForm

from nltk.tokenize import TreebankWordTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

@login_required(login_url="login")
def water_usage_view(request):
    person = Profile.objects.filter(person_of=request.user).last()
    form = WaterUsageForm(instance=person)
    arr = []
    if request.method == "POST":
        query = request.POST["searched"]
        query_vector = vectorizer.transform([query]).todense()
        similarity = cosine_similarity(query_vector, crop_vectors)
        ranks = (-similarity).argsort(axis=None)

        context = {
            "top_result": crops2[ranks[0]],
            "footprint": mp[crops2[ranks[0]]], 
        }

        return render(request,"water_usage.html", context)
    return render(request,"water_usage.html", {})

        # form = WaterUsageForm(request.POST, instance=person)
        # if form.is_valid():
        #     profile = form.save()
        #     profile.save()
        #     return redirect("home")

    # context = {"form":form}
    