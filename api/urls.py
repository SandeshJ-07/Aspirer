from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename="profile")
router.register("posts",PostViewSet, basename="post")
router.register("postimages",PostImagesViewSet, basename="postimages")
router.register("comments",CommentViewSet, basename="comment")
router.register("stories",StoryViewSet, basename="story")
router.register("chatrooms",ChatRoomViewSet, basename="chatroom")
router.register("chatmsgs",ChatMsgViewSet, basename="chatmsg")

urlpatterns = [
     path("",include(router.urls)),
]
