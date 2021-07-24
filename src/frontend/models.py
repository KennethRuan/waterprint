from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    person_of = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    water_usage = models.FloatField(default=0, null=True, blank=True)
    friends = models.ManyToManyField("Profile", null=True, blank=True)
    date = models.DateField(auto_now_add=True)
