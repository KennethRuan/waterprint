from django.contrib import admin
from django.urls import path
from .views import *
from .water_usage import *
from .friends import *

urlpatterns = [
    path('', login_view),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('water-usage/', water_usage_view, name="water-usage"),
    path('home/', home_view, name="home"),
    path('friends/', friends_view, name="friends"),
]
