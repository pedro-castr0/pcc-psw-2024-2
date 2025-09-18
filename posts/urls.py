from django.urls import path
from . import views

urlpatterns = [

    path('<int:id>', views.view, name='view_post'),
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('<int:id>/edit', views.edit, name='edit'),
    path('<int:id>/delete', views.delete, name='delete'),

]