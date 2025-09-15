from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('<str:name>/edit/', views.edit, name='edit'),
    path('<str:name>/delete/', views.delete, name='delete'),
    path('<str:name>/', views.view, name='view_community'),
    path('<str:name>/home/', views.home, name='home'),
    path('<str:name>/post/', views.post, name='post'),
    path('<str:name>/context/', views.context, name='context'),
    path("<str:name>/add-rule/", views.add_rule, name="add_rule"),
    path("<str:name>/rules/<int:rule_id>/edit/", views.edit_rule, name="edit_rule"),
    path("<str:name>/rules/<int:rule_id>/delete/", views.delete_rule, name="delete_rule"),
]