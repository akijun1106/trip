from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.post_create, name='post_create'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/edit/', views.mypage_edit, name='mypage_edit'),
    path('preference/', views.preference_settings, name='preference_settings'),
    path('plan/suggest/', views.plan_suggestion, name='plan_suggestion'),
    path('plan/history/', views.plan_history, name='plan_history'),
    path('plan/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]