from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username',)
    def save(self, *args, **kwargs):
        """
        Create and save a User with the given username and password.
        """
        data = self.cleaned_data
        account = Account(username=data["username"])
        account.set_password(data["password1"])
        account.save()
        friendlist = FriendList.objects.create(user=account)
        friendlist.save()
        return account
    
    def save_m2m(self):
        pass


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('username',)