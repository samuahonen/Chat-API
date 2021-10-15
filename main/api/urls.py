from .views import *
from django.urls import path,include


urlpatterns =  [
    path("test",Test.as_view()),
    path("message",MessageAPI.as_view()),
    path("friendlist",FriendListAPI.as_view()),
    path("friendrequest",FriendRequest.as_view()),
    path("addfriend",AddFriendAPI.as_view()),
    path("deletefriend",DeleteFriendAPI.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

]

