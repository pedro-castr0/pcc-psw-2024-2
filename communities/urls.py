from django.urls import path
from . import views

urlpatterns = [
    
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('<str:name>/edit/', views.edit, name='edit'),
    path('<str:name>/delete/', views.delete, name='delete'),
    path('<str:name>/', views.view, name='view'),
    path('<str:name>/home/', views.home, name='home'),
    path('<str:name>/post/', views.post, name='post'),
    path('<str:name>/context/', views.context, name='context'),

]