from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    person_of = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    water_usage = models.FloatField(default=0, null=True, blank=True)
    friends_list = models.ManyToManyField("Profile", default="users", blank=True, related_name="friends", symmetrical=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.person_of.username
    
    def add_friend(self, account):
        print(self.friends_list.all())
        if not account in self.friends_list.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends_list.all():
            self.friends.remove(account)
            self.save()