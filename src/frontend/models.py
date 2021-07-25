from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    person_of = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    water_usage = models.FloatField(default=0, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

class ProfileFollowing(models.Model):
    follower = models.ForeignKey("Profile", on_delete=models.CASCADE, name="follower")
    followed = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="followed")
    
