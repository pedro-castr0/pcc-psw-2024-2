from django.urls import path
from . import views

urlpatterns = [
    
    path('<int:id>', views.view, name='view'),
    path('edit/', views.edit, name='edit'),
    path('list/', views.list, name='list'),
    path('<int:id>/likes/', views.likes, name='likes'),
    path('<int:id>/dislikes/', views.dislikes, name='dislikes'),
    path('<int:id>/posts/', views.posts, name='posts'),
    path('<int:id>/comments/', views.comments, name='comments')

]