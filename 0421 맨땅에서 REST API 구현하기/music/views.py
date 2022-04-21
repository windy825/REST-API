from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Artist, Music
from .serializers import ArtistListSerializer, ArtistSerializer, MusicListSerializer, MusicSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def article_all(request):
    if request.method == 'GET':
        articles = get_list_or_404(Artist)
        serializer = ArtistListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Artist, pk=article_pk)
    serializer = ArtistSerializer(article)
    return Response(serializer.data)


@api_view(['POST'])
def music_create(request, article_pk):
    artist = get_object_or_404(Artist,pk=article_pk)
    serializer = MusicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(artist=artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def music_all(request):
    musics = get_list_or_404(Music)
    serializer = MusicListSerializer(musics, many=True)
    return Response(serializer.data)


@api_view(['GET','PUT','DELETE'])
def music(request, music_pk):
    target = get_object_or_404(Music, pk=music_pk)
    
    if request.method == 'GET':
        serializer = MusicSerializer(target)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MusicSerializer(target, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        target.delete()
        data = {
            '삭제된 음악 번호' : f'{music_pk} 번'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)