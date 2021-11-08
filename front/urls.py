from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = "Aspirer"

urlpatterns = [

    # Main Pages Urls
    path("",Home, name="Home"),
    path("login/",Login, name="Login"),
    path('signup/',Signup, name="SignUp"),
    path('logout/',Logout, name="Logout"),
    path("explore/",Explore, name="Explore"),
    path("profile/<str:username>/",ProfileView, name="Profile"),

    # eidtProile Urls
    path("editProfile/",EditProfile, name="EditProfile"),
    path("changePassword/",ChangePassword, name="ChangePassword"),
    path("privacy/",PrivacyandSecurity, name="Privacy"),
    path("loginActivity/",LoginActivity, name="LoginActivity"),
    path("downloadData/",DownloadData, name="DownloadData"),

    # Post
    path('post/upload',UploadPost, name="UploadPost"),
    path('togglePostLike/',TogglePostLike, name="TogglePostLike"),
    path('post/<int:pid>/',ViewPost, name="ViewPost"),
    path('togglePostSave/',TogglePostSave, name="TogglePostSave"),
    path('postComment/',PostComment, name="PostComment"),
    path('deletePost/',DeletePost, name="DeletePost"),
    path('toggleArchivePost/<int:pid>/',ToggleArchivePost, name="ToggleArchive"),
    
    # Story
    path('uploadStory/',UploadStory, name="UploadStory"),
    path("GetStory/<int:id>/",GetStory,name="GetStory"),
    path('deleteStory/', DeleteStory1, name="DeleteStory"),

    # Other Utils Urls
    path("checkUsername/",CheckUsername, name="checkUsername"),
    path("toggleFollow/<int:userId>/",ToggleFollow, name="ToggleFollow"),
    path("removeFollower/<int:userId>/",removeFollower, name="RemoveFollower"),
    path('handleFollowRequest/',HandleFollowRequest, name="HandleRequest"),
]

if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
