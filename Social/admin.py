from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import *

# Register your models here.
# admin.site.register(UserProfile)


# Unregister your models here.
admin.site.unregister(Group)

# Mix Profile info into User info
class ProfileInlie(admin.StackedInline):
    model = UserProfile

# Extend User Model
class CustomUserAdmin(admin.ModelAdmin):
    model= User
    # Just display username fields on admin page
    fields= ['username']
    inlines= [ProfileInlie]

# Unregister initial User
admin.site.unregister(User)

# Reregister User
admin.site.register(User, CustomUserAdmin)
admin.site.register(Twit)

