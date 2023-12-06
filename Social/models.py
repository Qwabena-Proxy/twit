from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows= models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False, blank= True
    )
    date_modified= models.DateTimeField(User, auto_now=True)
    # bio = models.TextField(max_length=255, blank=True, null=True)
    # image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
# Create twit model
class Twit(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.CharField(max_length= 200)
    twit_date= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return(
            f'{self.user} '
            f'({self.twit_date:%Y-%m-%d %H:%M}): '
            f'{self.body}'
        )

# Create Profile when User signs Up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile= UserProfile(user= instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender= User)
