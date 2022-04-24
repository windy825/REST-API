# REST API를 이용하여 Music app 구현하기

 <br>

<br>

### 0. urls.py 와 serializers.py

```python
# my_api/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('music.urls'))
]


# music/urls.py
urlpatterns = [
    path('articles/', views.article_all),  # GET, POST
    path('articles/<int:article_pk>/', views.article_detail),  # GET
    path('articles/<int:article_pk>/music/', views.music_create),  # POST
    path('music/', views.music_all),  # GET
    path('music/<int:music_pk>/', views.music),  # GET, PUT, DELETE
]
```

```python
# music/serializers.py

class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name',)


class MusicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id', 'title',)


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist')
        read_only_fields = ('artist',)


class ArtistSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True, read_only=True)
    music_cnt = serializers.IntegerField(source='music_set.count', read_only=True)
    
    class Meta:
        model = Artist
        fields = '__all__'
```

<br>

<br>

### 1. GET & POST api/v1/artists/

![제목 없음](https://user-images.githubusercontent.com/89068148/164396508-14aace77-c86e-4977-ad24-5eb4450376b5.png)

![제목 없음](https://user-images.githubusercontent.com/89068148/164405798-144f72b2-7d3e-456c-bbe2-d7c3d7d3009e.png)

```python
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
```

<br>

<br>

### 2. GET api/v1/artists/<artist_pk>/

![제목 없음](https://user-images.githubusercontent.com/89068148/164407952-d6173fe1-91b3-4c95-8ff4-6f28135c7dfe.png)

```python
@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Artist, pk=article_pk)
    serializer = ArtistSerializer(article)
    return Response(serializer.data)
```

<br>

<br>

### 3. POST api/v1/artists/<artist_pk>/music/

![제목 없음](https://user-images.githubusercontent.com/89068148/164409193-f2a05d54-4265-4252-8d4c-084f51efe583.png)

![제목 없음](https://user-images.githubusercontent.com/89068148/164409712-2b9c4502-1c1a-4d7a-8486-d8a88c751337.png)

```python
@api_view(['POST'])
def music_create(request, article_pk):
    artist = get_object_or_404(Artist,pk=article_pk)
    serializer = MusicSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(artist=artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

<br>

<br>

### 4. GET api/v1/music/

![제목 없음](https://user-images.githubusercontent.com/89068148/164410122-7b846b16-f05d-4879-a98a-a9300f170607.png)

```python
@api_view(['GET'])
def music_all(request):
    musics = get_list_or_404(Music)
    serializer = MusicListSerializer(musics, many=True)
    return Response(serializer.data)
```

<br>

<br>

### 5. GET & PUT & DELETE api/v1/music/<music_pk>/

![제목 없음](https://user-images.githubusercontent.com/89068148/164410606-11223224-d376-424d-b8c7-db6c65ef9d74.png)

![제목 없음](https://user-images.githubusercontent.com/89068148/164412233-30b3af3d-08c8-4d8e-9090-6e8195c0849b.png)

![제목 없음](https://user-images.githubusercontent.com/89068148/164411938-84de6fed-9f16-4f3a-81a1-7d5723dff4b1.png)

![제목 없음](https://user-images.githubusercontent.com/89068148/164412778-055c3425-0d65-43f5-8df3-0ba2491d063c.png)

```python
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
```

<br>

<br>