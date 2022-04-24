from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_index),
    path('<int:article_pk>/', views.articles_detail),
]
