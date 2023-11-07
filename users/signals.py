from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *


# @receiver(post_save,sender=User)
# def create_profile(sender,instance,created,**kwargs):
#     if created:
#         profile_personal_info.objects.create(user=instance)
        
# @receiver(post_save,sender=User)
# def save_profile(sender,instance,**kwargs):
#     x_instance = profile_personal_info(user=instance)
#     y_instance = profile_educational_and_career_info(profile_id=x_instance)
    # z_instance = profile_family_details(profile_id=x_instance)  
    # x_instance.save()
    # y_instance.save()
    # z_instance.save()