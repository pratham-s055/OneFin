from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions,authentication
from rest_framework.response import Response
from .serializers import UserSerializer, MovieSerializer, CollectionSerializer
from django.contrib.auth.models import User
import requests
from .utils import get_tokens_for_user, RequestCounterMiddleware

#importing models

from .models import Collection,Movie



"""
This was a best project i have worked on, all though , I didn't work on basic authentication
before so, I tried implementig that did a little research but coudn't add that feature.

rest everything is done, Please have a look
Thanks for your time..
Have a good day
"""


#configure env variables
import environ
env = environ.Env()
environ.Env.read_env()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_request_counts(request):

    """
    View to show request counts...
    """

    if request.method == 'GET':
        count = RequestCounterMiddleware.request_count
        return Response({"requests":count})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def reset_request_count(request):
    """
    View to reset a count..
    """
    reset_count = RequestCounterMiddleware.reset_counter
    return Response({"message":"request count reset successfully"})
        



@api_view(['POST','GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def movies_list(request):
    data = requests.get('https://demo.credy.in/api/v1/maya/movies/')
    data = data.json()
    return Response(data)


@api_view(['POST'])
def create_user(request):   
    """
    To create a user and return a jwt token
    """
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(username = serializer.data['username'])
    token = get_tokens_for_user(user)
    return Response(token)


@api_view(['POST','GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_collection(request):
    
    """
    Create a category for user
    """
    data = request.data
    if request.method == "POST":
        data['user'] = request.user.id
        
        serializer = CollectionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        collection = Collection.objects.get(title = data['title'])
        #add movies to the collection
        for movie in data['movies']:
            movie = Movie.objects.create(collection = collection, uuid = movie['uuid'], title = movie['title'],genre = movie['genre'])
            movie.save()

        #get uuid of the created category
        category = Collection.objects.get(title = serializer.data['title'], user = data['user'])
        resp = {
            "uuid" : category.id
        }
    elif request.method == "GET":
        collection = Collection.objects.filter(user = request.user.id)
        print(collection)
        data_lst = []
        for data in collection:
            print(data)
            data_lst.append({
                "title" : data.title,
                "description" : data.description,
                "uuid" : data.uuid,
            })

        return Response({"data":data_lst})
    
    return Response(resp)


@api_view(['POST','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def collection_update(request,pk):
    """
    view to update collection..
    """
    movie_list = []
    if request.method == "PUT":
        
        collection = Collection.objects.get(user = request.user.id, id = pk)
        for movie in request.data['movies']:
            movies = Movie.objects.create(collection = collection, title = movie['title'], genre = movie['genre'], uuid = movie['uuid'])
            movies.save()
    elif request.method == "DELETE":
        collection = Collection.objects.get(id = pk)
        collection.delete()
        return Response({"DELETE": "successful"})

    movies = Movie.objects.filter(collection=collection)

    print(movies)
    for data in movies:
        movie_list.append(
            {
                "title":data.title,
                "genre":data.genre,
                "uuid": data.uuid
            }
        )
    resp = {
        "title" : collection.title,
        "description" : collection.description,
        "movies" : movie_list
    }
    return Response(resp)




@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def movies(request):
    
    """
    Create Movies and update movies
    """
    data = request.data
    data['user'] = request.user.id
    serializer = MovieSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"created":"success"})