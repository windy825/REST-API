from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import ArticleListSerializer, ArticleSerializer, CommentListSerializer

from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Article, Comment
from articles import serializer

# Create your views here.

@api_view(['GET', 'POST'])
def articles_index(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def articles_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data) 

    elif request.method == 'PUT':
        serializer = ArticleSerializer(instance=article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        data = {
            'data':article_pk,
        }
        return Response(data)


@api_view(['GET'])
def comment_list(request):
    comments = get_list_or_404(Comment)
    serializer = CommentListSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def comment_detail(request, comment_pk):

    comment = get_object_or_404(Comment, pk=comment_pk)
    serializer = CommentListSerializer(comment)
    return Response(serializer.data)

@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data)