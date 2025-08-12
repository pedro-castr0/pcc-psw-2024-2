from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.view, name='view'),
    path('update/', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('list/', views.list, name='list')
]