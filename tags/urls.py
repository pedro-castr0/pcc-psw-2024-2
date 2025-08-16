from django.urls import path
from . import views

urlpatterns = [
    
    path('autocomplete/', views.tag_autocomplete, name='tag-autocomplete'),
    path('tags/', views.tags_list, name='tags_list'),
    path('search/', views.search_tags, name='search_tags'),
    
]
