from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
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
    master_list = MasterList.objects.filter(user=request.user).last()
    form = WaterUsageForm(instance=person)
    context = {}
    context["stage"]=1

    if request.method == "POST":
        if 'search' in request.POST:
            query = request.POST["searched"]
            query_vector = vectorizer.transform([query]).todense()
            similarity = cosine_similarity(query_vector, crop_vectors)
            ranks = (-similarity).argsort(axis=None)
            request.session["food_item"] = crops2[ranks[0]]
            request.session["footprint"] = mp[crops2[ranks[0]]]

            context["top_result"] = crops2[ranks[0]];
            context["footprint"] = mp[crops2[ranks[0]]]
            context["stage"] = 2;
        
        if 'add-item' in request.POST:
            if request.session["new_food_list"]:
                FoodList.objects.create(user=request.user, master_list=master_list)
                request.session["new_food_list"] = False

            request.session["search_occured"] = True
            food_item = request.session["food_item"]
            quantity = request.POST["quantity"]
            footprint = float(request.session["footprint"]) * float(quantity)
            
            profile = Profile.objects.filter(person_of=request.user).last()
            profile.water_usage += footprint
            profile.save()

            FoodItem.objects.create(food=food_item, footprint=footprint, food_list=FoodList.objects.filter(user=request.user).last())
            context["stage"] = 1;

        for key in request.POST:
            if 'delete' in key:
                try:
                    context["stage"] = 1;
                    delete_ind = int(key.split('-')[1])
                    food_list_id = FoodList.objects.filter(user=request.user).last()
                    food_list = FoodItem.objects.filter(food_list=food_list_id)
                    r = food_list.order_by('id')[delete_ind]
                    r.delete()
                except IndexError:
                    print("An index error occured, likely that the page was refreshed after a delete request")
        
    
    if request.session["search_occured"]:
        food_list_id = FoodList.objects.filter(user=request.user).last()
        context["food_list"] = FoodItem.objects.filter(food_list=food_list_id)
    # print(context["stage"])

    return render(request,"water_usage.html", context)

        # form = WaterUsageForm(request.POST, instance=person)
        # if form.is_valid():
        #     profile = form.save()
        #     profile.save()
        #     return redirect("home")

    # context = {"form":form}
    