from rest_framework import serializers
from .models import *
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id","username")

class MessageSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    sender = UserSerializer(read_only=True)
    date = serializers.TimeField(read_only=True)
    recipient_username = serializers.CharField(write_only=True)
    class Meta:
        model = Message
        fields = ("msg","recipient","sender","date","recipient_username")  

    def create(self,recipient,sender,msg):
        recipient = get_object_or_404(Account,username=recipient)
        friendlist = FriendList.objects.get(user=sender.id)
        if recipient in friendlist.all_friends.all():
            msg = Message.objects.create(msg=msg,sender=sender,recipient=recipient)
            msg.save()
            return msg
        return False
    


class FriendListSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    all_friends = UserSerializer(read_only=True, many=True)

class CustomRegisterSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username','password', 'password2',]
        extra_kwargs = {
            'password': {
                'write_only':True
            }
        }

    def save(self,p1):
        user = Account(
            username=self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        user.set_password(password)
        user.save()
        friendlist = FriendList.objects.create(user=user)
        friendlist.save()
        return user