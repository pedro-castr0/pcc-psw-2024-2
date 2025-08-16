from django.urls import path
from . import views

urlpatterns = [
    
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/', views.view, name='view'),
    path('<int:id>/home/', views.home, name='home'),
    path('<int:id>/post/', views.post, name='post'),
    path('<int:id>/context/', views.context, name='context'),

]