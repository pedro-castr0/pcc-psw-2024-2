from django.urls import path
from . import views

urlpatterns = [
    path('comment/', views.comment, name='comment'),
    path('list/', views.list, name='list'),
    path('<int:id>/', views.view, name='view'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('list/', views.list, name='list'),
]