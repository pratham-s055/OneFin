from django.urls import path
from . import views

from . import views



urlpatterns = [
    #Movies-Collection urls
    path('movies',views.movies_list, name = 'movies_list'),
    path('collection',views.create_collection, name = 'collection'),
    path('collection/<str:pk>',views.collection_update, name = 'collection'),

    #request Count
    path('request-count',views.get_request_counts, name = 'request-count'),
    path('request-count-reset',views.reset_request_count, name = 'request-count-reset'),

    #user registration 
    path('request-count',views.create_user, name = 'request-count'),
    

]