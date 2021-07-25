from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    person_of = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    water_usage = models.FloatField(default=0, null=True, blank=True)
    total_usage = models.FloatField(default=0, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

class ProfileFollowing(models.Model):
    follower = models.ForeignKey("Profile", on_delete=models.CASCADE, name="follower")
    followed = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="followed")
    
class FoodItem(models.Model):
    food = models.CharField(default="", null=True, blank=True, max_length=150)
    footprint = models.FloatField(default=0, null=True, blank=True)
    food_list = models.ForeignKey("FoodList", on_delete=models.CASCADE, related_name="foods")

class FoodList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    master_list = models.ForeignKey("MasterList", on_delete=models.CASCADE, related_name="master_list")

class MasterList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
