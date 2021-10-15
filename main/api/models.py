from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.shortcuts import get_object_or_404
from .managers import CustomUserManager
from django.utils import timezone
# Create your models here.

class Account(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(unique=True, null=True,max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    test = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Message(models.Model):
    msg = models.TextField()
    recipient = models.ForeignKey(Account,related_name="recipient",on_delete=models.CASCADE)
    date = models.TimeField(auto_now_add=True)
    sender = models.ForeignKey(Account,related_name="sender", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender}, msg:{self.msg} to {self.recipient} ({self.date})"

class FriendList(models.Model):
    user = models.OneToOneField(Account,related_name="user", on_delete=models.CASCADE)
    all_friends = models.ManyToManyField(Account,related_name="all_friends",blank=True)
    request = models.ManyToManyField(Account, related_name="request", blank=True)    

    def add_friend(self,id):
        if get_object_or_404(FriendList,user=id):
            self.all_friends.add(id)
            self.request.remove(id)
            self.save()
            friend = FriendList.objects.get(user=id)
            friend.all_friends.add(self.user.id)
            friend.save()
            return True
        return False
    
    def delete_friend(self,id):
        friend = Account.objects.get(pk=id)
        if friend in self.all_friends.all():
            self.all_friends.remove(id)
            self.save()
            friend = FriendList.objects.get(user=id)
            friend.all_friends.remove(self.user.id)
            friend.save()
            return True
        return False


    def __str__(self):
        return self.user.username
    


class ChatGroup(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(Account)

    def __str__(self):
        return self.name


