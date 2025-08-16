from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join, name='join'),
    path('list/', views.list, name='list'),
    path('leave/', views.leave, name='leave')
]