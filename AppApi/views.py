from django.shortcuts import render ,redirect
from .models import Register
from .serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework import status

class RegisterAPI(GenericAPIView,ListModelMixin,CreateModelMixin):
     queryset=Register.objects.all()
     serializer_class=RegisterSerializer
     def post(self,request,*args,**Kwargs):
          print(request.data)
          print(request.POST)
          return self.create(request,*args,**Kwargs)
     def get(self,request,*args,**Kwargs):
          return self.list(request,*args,**Kwargs)