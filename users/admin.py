from django.contrib import admin
from .models import *

admin.site.register(profile_personal_info)
admin.site.register(profile_educational_and_career_info)

admin.site.register(profile_family_details)
admin.site.register(partner_preferences)
admin.site.register(Bookmark)
admin.site.register(FriendRequest)

# Register your models here.
