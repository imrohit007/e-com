from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from .serializers import *
from django.contrib.auth.models import User
from ..models import *
from rest_framework import generics

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer