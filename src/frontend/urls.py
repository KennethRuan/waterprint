from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('home/', home_view, name="home"),
]
