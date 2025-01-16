from rest_framework import serializers
from .models import User,Chat
import datetime

class Userser(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["name","uname","pas"]
class Chatser(serializers.ModelSerializer):
    time = serializers.DateTimeField()
    class Meta:
        model=Chat
        fields=["sen","rec","mess","time"]