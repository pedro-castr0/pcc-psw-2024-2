from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.view, name='view'),
    path('update/', views.update, name='update'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('list/', views.list, name='list'),
    path('<int:id>/likes/', views.likes, name='likes'),
    path('<int:id>/dislikes/', views.dislikes, name='dislikes'),
    path('<int:id>/posts/', views.posts, name='posts'),
    path('<int:id>/comments/', views.comments, name='comments')
]