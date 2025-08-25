from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.edit, name='edit'),
    path('list/', views.list, name='list'),
    path('<str:username>/', views.view, name='view'),
    path('<str:username>/likes/', views.likes, name='likes'),
    path('<str:username>/dislikes/', views.dislikes, name='dislikes'),
    path('<str:username>/posts/', views.posts, name='posts'),
    path('<str:username>/comments/', views.comments, name='comments')

]