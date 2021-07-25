from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    person_of = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    water_usage = models.FloatField(default=0, null=True, blank=True)
    friends_list = models.ManyToManyField(User, default="users", blank=True, related_name="friends")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.person_of.username
    
    def add_friend(self, account):
        if not account in self.friends_list.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends_list.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, removee):
        remover_friends_list  = self.friends_list
        remover_friends_list.remove_friend(removee)
        friends_list = Profile.objects.get(person_of=removee)
        friend_list.remove_friend(self.person_of)
    
    def friend(self, account):
        friender_friends_list = self.friends_list
        friender_friends_list.add_friend(account)
        friends_list = Profile.objects.get(person_of=account)
        friends_list.add_friend(self.person_of)