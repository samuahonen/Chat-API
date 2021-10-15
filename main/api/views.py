from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class Test(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response("test")

class MessageAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    #create new message
    def post(self,request):
        serializer = MessageSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response({"msg":"error"}, status=status.HTTP_404_NOT_FOUND)
        msg = serializer.create(request.POST["recipient_username"],request.user,request.POST["msg"])
        if msg != False:
            serializer = MessageSerializer(msg)
            return Response(serializer.data)
        return Response({"msg":"error"},status=status.HTTP_404_NOT_FOUND)

    #get message
    def get(self,request):
        if not "username" in request.GET:
            return Response({"msg":"error"}, status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(Account,username=request.GET["username"])
        messages = Message.objects.filter(recipient=user.id)
        serializer = MessageSerializer(messages,many=True)
        return Response(serializer.data)
    
class FriendListAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        friendlist = FriendList.objects.get(user=request.user.id)
        serializer = FriendListSerializer(friendlist)
        return Response(serializer.data)

class FriendRequest(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if not "id" in request.GET:
            return Response({"msg":"error"}, status=status.HTTP_404_NOT_FOUND)
        friendlist = get_object_or_404(FriendList,user=request.GET["id"])
        friendlist.request.add(request.user.id)
        friendlist = FriendList.objects.get(user=request.user.id)
        serializer = FriendListSerializer(friendlist)
        return Response("friendlist.data")


class AddFriendAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if not "id" in request.GET:
            return Response({"msg":"error"}, status=status.HTTP_404_NOT_FOUND)
        friendlist = get_object_or_404(FriendList,user=request.user.id)
        friendlist.add_friend(request.GET["id"])
        serializer = FriendListSerializer(friendlist)
        return Response(serializer.data)

class DeleteFriendAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if not "id" in request.GET:
            return Response({"msg":"error"}, status=status.HTTP_404_NOT_FOUND)
        friendlist = FriendList.objects.get(user=request.user.id)
        friendlist.delete_friend(request.GET["id"])
        serializer = FriendListSerializer(friendlist)
        return Response(serializer.data)

