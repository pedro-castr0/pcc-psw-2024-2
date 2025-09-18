from django.urls import path
from . import views

urlpatterns = [
    path('follow/', views.follow, name='follow'),
    path('list/', views.list, name='list'),
    path('unfollow/', views.unfollow, name='unfollow')
]