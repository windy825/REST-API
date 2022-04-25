from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.articles_index),
    path('articles/<int:article_pk>/', views.articles_detail),
    path('articles/<int:article_pk>/comments/', views.comment_create),

    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
]
