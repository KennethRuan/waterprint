from django.contrib import admin
from .models import Profile, ProfileFollowing

# Register your models here.
admin.site.register(Profile)
admin.site.register(ProfileFollowing)
