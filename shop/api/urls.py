from ..models import *
from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'category', CategoryViewSet)

router.register(r'products', ProductsViewSet)


path(r'<pk>', include(router.urls)),