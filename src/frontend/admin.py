from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(ProfileFollowing)
admin.site.register(FoodItem)
admin.site.register(FoodList)
admin.site.register(MasterList)
