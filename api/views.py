from django.shortcuts import render
from rest_framework import viewsets
from front.models import *
from .serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostImagesViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = PostImages.objects.all()
    serializer_class = PostImagesSerializer

class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class StoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Story.objects.all()
    serializer_class = StorySerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatMsgViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    throttle_classes = (AnonRateThrottle,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ChatMsg.objects.all()
    serializer_class = ChatMsgSerializer