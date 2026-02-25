from django.contrib import admin
from .models import Destination, TravelPost, UserPreference, TravelPlan, TravelRoute

class TravelPostAdmin(admin.ModelAdmin):
    """旅行投稿の管理画面設定"""
    # 出発地点、到着地点、経由地点を除外
    exclude = ('start_point', 'end_point', 'via_points')
    
    list_display = ('photo_location', 'category', 'transportation', 'cost', 'user', 'created_at')
    list_filter = ('category', 'transportation', 'created_at')
    search_fields = ('photo_location', 'content')
    readonly_fields = ('created_at',)

admin.site.register(Destination)
admin.site.register(TravelPost, TravelPostAdmin)
admin.site.register(UserPreference)
admin.site.register(TravelPlan)
admin.site.register(TravelRoute)
