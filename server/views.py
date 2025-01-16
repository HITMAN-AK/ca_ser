from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import User,Chat
from .serializers import Userser,Chatser
from datetime import datetime

class Log(APIView):
    def post(self, request):
        uname = request.data.get("uname")
        pas = request.data.get("pas")
        try:
            user = User.objects.get(uname=uname) 
        except User.DoesNotExist:
            return Response({"status": False})
        if pas == user.pas:
            return Response({"status": True})
        else:
            return Response({"status": False})

class Signup(APIView):
    def post(self, request):
        uname = request.data.get("uname")
        if User.objects.filter(uname=uname).exists():
            return Response(
                {"status": False}
            )
        serializer = Userser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status":True}
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Cuname(APIView):
    def post(self, request):
        uname = request.data.get("uname")
        try:
            user = User.objects.get(uname=uname) 
            return Response({"available": False})
        except User.DoesNotExist:
            return Response({"available": True})

class Users(APIView):
    def get(self, request):
        ud = User.objects.all()  
        serializer = Userser(ud, many=True)  
        return Response(serializer.data)  

class FetchMessages(APIView):
    def post(self, request):
        sender = request.data.get('sen')
        receiver = request.data.get('rec')
        messages = (
            Chat.objects.filter(sen=sender, rec=receiver) |
            Chat.objects.filter(sen=receiver, rec=sender)
        )
        messages = sorted(messages, key=lambda x: x.time) 
        serializer = Chatser(messages, many=True)
        return Response(serializer.data)
class StoreMessages(APIView):
    def post(self, request):
        sender = request.data.get("sen")
        receiver = request.data.get("rec")
        message = request.data.get("mess")
        
        current_time = datetime.now()
        
        data = {
            'sen': sender,
            'rec': receiver,
            'mess': message,
            'time': current_time,  
        }
        
        serializer = Chatser(data=data)  
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True})
        else:
            return Response(serializer.errors, status=400)