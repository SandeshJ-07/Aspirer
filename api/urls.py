from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename="profile")

urlpatterns = [
     path("profileapi",include(router.urls)),
]
