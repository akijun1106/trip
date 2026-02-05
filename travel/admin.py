from django.contrib import admin
from .models import Destination, TravelPost, UserPreference, TravelPlan, TravelRoute

admin.site.register(Destination)
admin.site.register(TravelPost)
admin.site.register(UserPreference)
admin.site.register(TravelPlan)
admin.site.register(TravelRoute)
