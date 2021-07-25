from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, MasterList
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(person_of=instance)
        MasterList.objects.create(user=instance)
        print("Created Profile")
        
post_save.connect(create_profile,sender=User)