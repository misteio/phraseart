from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('citations', views.all_quotes, name='quotes'),
    path('recherche', views.search, name='search'),
    path('citation/tag/<slug:tag_slug>/', views.tag_list, name='quote_tag_list'),
    path('citation/auteur/<slug:author_slug>/', views.author_list, name='quote_author_list'),
    path('citation/<slug:slug>/', views.quote, name='quote'),
]