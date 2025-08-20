from django.urls import path
from . import views

app_name = "users" 
urlpatterns = [
    
    path('create/', views.create, name='create'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('list/', views.list, name='list'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),

]