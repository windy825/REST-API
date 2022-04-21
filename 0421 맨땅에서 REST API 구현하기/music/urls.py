from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_all),  # GET, POST
    path('articles/<int:article_pk>/', views.article_detail),  # GET
    path('articles/<int:article_pk>/music/', views.music_create),  # POST
    path('music/', views.music_all),  # GET
    path('music/<int:music_pk>/', views.music),  # GET, PUT, DELETE
]