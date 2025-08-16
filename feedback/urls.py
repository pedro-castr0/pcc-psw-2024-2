from django.urls import path
from . import views

urlpatterns = [

    path('', views.feedback, name='feedback'),
    path('null_feedback/', views.null_feedback, name='null_feedback'),
    path('list/', views.list, name='list')
    
]