from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join, name='join'),
    path('list/', views.list, name='list'),
    path('unjoin/<int:id>', views.unjoin, name='unjoin')
]