from rest_framework import serializers
from ..models import *
from django.contrib.auth.models import User

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'name', 'slug', 'image', 'description', 'price',)