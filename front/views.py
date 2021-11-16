from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.management import call_command
import os
import cv2
from django.contrib.auth.hashers import check_password
# Create your views here

# Views
def Login(request):
    error = False
    not_exist = False
    us = ""
    if request.method == "POST":
        x = request.POST
        us = x['username']
        pa = x['password']
        username = User.objects.filter(Q(email = us) | Q(username = us))
        if username.exists():
            username = username[0]
        else:
            username = None
        user = authenticate(username=username, password=pa)
        data = User.objects.filter(username=username)
        if user:
            login(request, user)
            return redirect('Aspirer:Home')
        else:
            if data:
                error = True
            else:
                not_exist=True
    d = {"error": error, "not_exist": not_exist, "username":us,"act": "login"}
    return render(request, 'login.html',d)


def Signup(request):
    already = False
    if request.method == "POST":
        x = request.POST
        email = ""
        contact = ""
        a = x['email']
        if "@" in a:
            email = a
        else:
            contact = a
        fullname = x['fname']
        username = x['username']
        password = x['password']
        data = User.objects.filter(Q(email = a) | Q(username = username))
        data1 = Profile.objects.filter(contact = a)
        if(data or data1):
            already = True
        else: 
            lasName = " "
            firName = ' '
            fname = fullname.split()
            if fname[0]:
                firName = fname[0]
            if len(fname) > 1:
                lasName = fname[1]
            user = User.objects.create_user(username=username,email=email,first_name=firName,last_name=lasName,password=password)
            p = Profile.objects.create(user = user, contact = contact, Email = email, username=username)
            p.following.append(str(3))
            Main = Profile.objects.get(id = 3)
            Main.followers.append(str(p.id))
            Main.save()
            p.save()
            return render(request,'login.html',{"act":"login"})
    d = {"already":already, "act": "signup"}
    return render(request,'login.html',d)


@login_required(login_url='/login/')
def Logout(request):
    logout(request)
    return redirect('Aspirer:Login')


@login_required(login_url='/login/')
def Home(request):
    call_command('deleteStory')
    CProfile = Profile.objects.get(user = request.user)
    posts = []
    for i in Post.objects.filter(Q(user__in = CProfile.following), Q(archived = False)).order_by('-id'):
        comments = Comment.objects.filter(Post = i)
        posts.append({"post":i,"comments":comments})
    
    userStory = Story.objects.filter(User = request.user)
    if userStory:
        userStory = userStory[0]
    else:
        userStory = 0

    stories = []
    for i in CProfile.following:
        P1 = Story.objects.filter(User__id = i)
        if P1.exists():
            P = P1[0]
            RProfile = Profile.objects.filter(user = i)[0]
            if str(request.user.id) in RProfile.hide_story:
                continue
            if P.type == "c" and str(request.user.id) not in RProfile.close_friends:
                continue
            stories.append({"user":i, "stories":P,"RProfile":RProfile}) 
    dic = {"posts":posts, "active":"home", "CProfile":CProfile, "userStory":userStory, "stories":stories}
    return render(request,'home.html',dic)

def Explore(request):
    CProfile = Profile.objects.get(user = request.user)
    posts = []
    for i in Post.objects.filter(Q(user__in = CProfile.following) | Q(profile__pvt_acc = 0), Q(archived = False)).order_by('-id'):
        posts.append(i)
    dic = {"active":"explore", "posts":posts, "CProfile":CProfile}  
    return render(request,'explore.html',dic)    

@login_required(login_url='/login/')
def ProfileView(request,username):
    CUser = request.user
    RUser = User.objects.get(username = username)
    CProfile = Profile.objects.get(user = request.user)
    RProfile = Profile.objects.get(user = RUser)

    Posts = Post.objects.filter(user = RUser, archived = False)
    followers = []
    suggestion = []
    followings = []
    archived = Post.objects.filter(user = RUser, archived = True) 
    for i in RProfile.followers:
        followers.append(Profile.objects.get(user__id = i))

    for i in RProfile.following:
        followings.append(Profile.objects.get(user__id = i))

    for i in Profile.objects.all():
        if i.user != RUser and i not in followings:
                suggestion.append(i)

    dic = {"active":"profile", "CUser": CUser,"RUser":RUser, "CProfile":CProfile, "RProfile":RProfile, "Posts":Posts, "followers":followers, "followings":followings, "suggestions":suggestion, "archived":archived}
    return render(request,'profile.html',dic)

@login_required(login_url='/login/')
def EditProfile(request):
    CUser = request.user
    CProfile = Profile.objects.get(user = request.user)
    gender =  [
        {"a":'M',"b":"Male"},
        {"a":"F","b":"Female"},
        {"a":"N","b":"Prefer Not To Say"}
    ]

    imgurl = CProfile.ProfileImg.path

    if request.method == "POST":
        x = request.POST
        if "editprofileBtn" in x:
            u = User.objects.filter(username= x.get('username'))
            if u.exists() and x.get('username') != CUser.username:
                print("N")
            else:
                CProfile.username = x.get('username')
                CProfile.Email = x.get('email')
                CProfile.contact = x.get('contact')
                CProfile.gender = x.get('gender')
                CProfile.website = x.get('website')
                CProfile.bio = x.get('bio')
                CUser.username=x.get('username')
                CUser.email = x.get('email')
                CUser.first_name = x.get('name').split()[0]
                CUser.last_name = x.get('name').split()[1]
                CUser.save()
                CProfile.save()
        if "image" in x:
            if imgurl.endswith("default.png"):
                print("Default")
            else:
                os.remove(imgurl)
            CProfile.ProfileImg = request.FILES["newProfileImg"]
            CProfile.save()
            imm = CProfile.ProfileImg
            img_path = imm.path
            img_name = str(imm)
            new_img = resize_img(img_path, img_name, "profile")
            CProfile.ProfileImg = new_img
            CProfile.save()
            return redirect("Aspirer:EditProfile")
                
    dic = {"active":"profile", "CProfile":CProfile, "gender":gender, "act": "EditProfile","title":"Edit Profile"}
    return render(request,'editprofile.html',dic)

@login_required(login_url='/login/')
def ChangePassword(request):
    CProfile = Profile.objects.get(user = request.user)
    CUser = User.objects.get( id = request.user.id )
    has_password = False

    if request.user.has_usable_password:
        has_password = True

    if request.POST:
        password = request.user.password
        currPass = request.POST.get('CurrPass')
        newPass = request.POST.get('NewPass')
        rePass = request.POST.get('rePass')

        if not(has_password):
            if(newPass==rePass):
                request.user.set_password(newPass)
                request.user.save()
                return redirect('Aspirer:Profile',username=request.user.username)
            else:
                return render(request, 'editProfile.html',{'alert_flag':True,'msg':"New Password and Re-entered Password does not match!",'has_password':has_password, "CProfile": CProfile, "act":"ChangePassword", "active": "profile","title":"Change Password"})

        matchcheck = check_password(currPass,password)
        if matchcheck:
            if not(newPass == currPass):
                if newPass==rePass:
                    request.user.set_password(newPass)
                    request.user.save()
                    return redirect('Aspirer:Profile',username = request.user.username)
                else:
                    return render(request, 'editProfile.html',{'alert_flag':True,'msg':"New Password and Re-entered Password does not match!",'Password':has_password, "CProfile": CProfile, "act":"ChangePassword", "active": "profile","title":"Change Password"})
            elif newPass==currPass:
                    return render(request, 'editProfile.html',{'alert_flag':True,'msg':"New Password cannot be Old Password!",'Password':has_password, "CProfile": CProfile, "act":"ChangePassword", "active": "profile","title":"Change Password"})
        else:      
            return render(request, 'editProfile.html',{'alert_flag':True,'msg':"Current Password Does not match",'Password':has_password, "CProfile": CProfile, "act":"ChangePassword", "active": "profile","title":"Change Password"})

    dic = {"active":"profile", "CProfile":CProfile, "act": "ChangePassword", "has_password": has_password, 'alert_flag': False,"title":"Change Password"}
    return render(request,'editprofile.html',dic)

@login_required(login_url='/login/')
def PrivacyandSecurity(request):
    CProfile = Profile.objects.get(user = request.user)
    hidden = []
    others= []

    for i in CProfile.hide_story:
        hidden.append(Profile.objects.get(user__id = i))
    for i in CProfile.followers:
        if i not in CProfile.hide_story:
            others.append(Profile.objects.filter(user__id = i)[0])

    if request.POST:
        x = request.POST
        action = x.get('action')
        if action == 'togglePrivacy':
            CProfile.pvt_acc = not(CProfile.pvt_acc)
            r = CProfile.follow_request
            f = CProfile.followers
            for req in r:
                RUser = User.objects.filter( id = req )[0]
                RProfile =  Profile.objects.filter( user = RUser )[0]
                z = RProfile.following
                z.append(request.user.id)
                RProfile.following = z
                RProfile.save()
                f.append(req)
                r.remove(req)
            CProfile.followers = f
            CProfile.follow_request = r
            CProfile.save()
        if action == 'toggleActivtiy':
            CProfile.activity_status = not(CProfile.activity_status)
            CProfile.save()
        if action == 'toggleStory':
            CProfile.story_share = not(CProfile.story_share)
            CProfile.save()

    dic = {"active":"profile", "CProfile":CProfile, "act": "PrivacyAndSecurity", "title":"Privacy and Security","hidden":hidden, "others":others}
    return render(request,'editprofile.html',dic)

@login_required(login_url='/login/')
def LoginActivity(request):
    CProfile = Profile.objects.get(user = request.user)

    dic = {"active":"profile", "CProfile":CProfile, "act": "LoginActivity","title":"Login Activity"}
    return render(request,'editprofile.html',dic)

@login_required(login_url='/login/')
def DownloadData(request):
    CProfile = Profile.objects.get(user = request.user)

    dic = {"active":"profile", "CProfile":CProfile, "act": "DownloadData","title":"Download Data"}
    return render(request,'editprofile.html',dic)

# Check if username exists
@csrf_exempt
def CheckUsername(request):
    exist = False
    if request.method == "GET":
        us = request.GET.get('username')
        Pro = Profile.objects.filter(username = us)   
        if Pro.exists():
            exist = True
    return JsonResponse({"exist":exist})


# Post Views
def UploadPost(request):
    CProfile = Profile.objects.get(user = request.user)
    CUser = request.user
    
    if request.method=="POST":
        x = request.POST
        caption = x['caption']
        location = x['location']
        Images = request.FILES.getlist('images')       
        showimage =Images[0]
        comments = False
        if x.get('comments') == "on":
            comments = True
        p = Post.objects.create(user=CUser,caption=caption, Location = location, Showimage = showimage, shares = 0,saved=0, profile = Profile.objects.get(user = CUser), allow_comments = comments )
        imm = p.Showimage
        img_name = str(imm)
        img_path = imm.path
        new_img = resize_img(img_path, img_name, "post")
        p.Showimage = new_img
        p.save()
        #creating image objects
        for image in Images[1:]:
            photo = PostImages.objects.create(Post = p , image=image)
            photo.save()
            imm = photo.image
            img_name = str(imm)
            img_path = imm.path
            new_img = resize_img(img_path, img_name, "post")
            photo.image = new_img
            photo.save()
        return redirect('Aspirer:Profile',username=request.user.username)
    dic = {"active":"upload"}
    return render(request, "uploadPost.html",dic)


# Utility Functions
# Resize Image
def resize_img(img_path, img_name, type):
    pic=cv2.imread(img_path)
    if type == "post":
        width = 1080
        height = 1080

    if type == "profile":
        width = 250
        height = 250
    
    dim = (width, height)
    img_pic = cv2.resize(pic, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite('media/'+img_name, img_pic)

    return img_name

def ToggleFollow(request, userId):
    status = ' '
    text = ' '
    RProfile = Profile.objects.get(user__id = userId)
    CProfile = Profile.objects.get(user = request.user)
    RId = request.user.id

    # Unfollow user
    if str(RId) in RProfile.followers:
        RProfile.followers.remove(str(RId))
        CProfile.following.remove(str(RProfile.user.id))
        status = 'Unfollow'
        text = 'Follow'
    # Remove the requested
    elif str(RId) in RProfile.follow_request:
        RProfile.follow_request.remove(str(RId))
        status = 'UnRequest'
        text = 'Follow'
    # Follow the user
    else:
        if not(RProfile.pvt_acc):
            RProfile.followers.append(str(RId))
            CProfile.following.append(str(RProfile.user.id))
            status = 'Follow'
            text = 'Unfollow'
        elif RProfile.pvt_acc:
            RProfile.follow_request.append(str(RId))
            status = 'Requested'
            text = 'Requested'

    RProfile.save()
    CProfile.save()
    return JsonResponse({'data':status, "text":text})


def removeFollower(request,userId):
    RProfile = Profile.objects.get(user__id = userId)
    CProfile = Profile.objects.get(user = request.user)
    if str(RProfile.user.id) in CProfile.followers:
        CProfile.followers.remove(str(userId))

    if str(request.user.id) in RProfile.following:
        RProfile.following.remove(str(request.user.id))

    CProfile.save()
    RProfile.save()
    return JsonResponse({"data":"success"})


def HandleFollowRequest(request):
    if request.POST:
        x = request.POST
        action = x.get('action')
        id = x.get('id')
        CProfile = Profile.objects.get(user = request.user)
        RProfile = Profile.objects.get(user__id = id)
        if action == 'Accept':
            if str(id) not in CProfile.followers:
                CProfile.followers.append(str(id))
                RProfile.following.append(str(request.user.id))
            if str(id) in CProfile.follow_request:
                CProfile.follow_request.remove(str(id))

        elif action == 'Reject':
            if str(id) in CProfile.follow_request:
                CProfile.follow_request.remove(str(id))

        CProfile.save()
        RProfile.save()
        return JsonResponse({'data':action})

def ToggleBlockUser(request,uid):
    if request.POST:
        id = uid
        CProfile = Profile.objects.get(user = request.user)
        if str(id) in CProfile.blocked_users:
            CProfile.blocked_users.remove(str(id))
            text='Unblocked'
        else:
            CProfile.blocked_users.append(str(id))
            text='Blocked'
        CProfile.save()
        return JsonResponse({'data':text})

def ToggleRestrictUser(request,uid):
    if request.POST:
        id=uid
        CProfile = Profile.objects.get(user = request.user)
        if str(id) in CProfile.restricted_users:
            CProfile.restricted_users.remove(str(id))
            text="Unrestricted"
        else:
            CProfile.restricted_users.append(str(id))
            text = 'Restricted'
        CProfile.save()
        return JsonResponse({"data":text})

# Post Views
def ViewPost(request,pid):
    post = Post.objects.get(id = pid)
    try:
        PostImage = PostImages.objects.get(Post= post)
    except:
        PostImage = None
    CProfile = Profile.objects.get(user = request.user)
    RProfile = Profile.objects.get(user = post.user)
    if (str(request.user.id) not in RProfile.followers and RProfile.pvt_acc and post.user != request.user) or (post.archived and post.user != request.user):
        return redirect('Aspirer:Profile',username=post.user.username)
    otherPosts = Post.objects.exclude(id = pid).filter(user = post.user)
    dic = {'CProfile' : CProfile, 'RProfile':RProfile, 'Post':post, 'postImgs':PostImage, 'otherPosts':otherPosts} 
    return render(request,'post.html',dic)

def TogglePostLike(request):
    if request.POST:
        print("X")
        id = request.user.id
        x = request.POST
        pid = x.get('pid')
        post = Post.objects.get(id = pid)
        if post.archived:
            return redirect('Aspirer:Profile',username=post.user.username)
        if str(id) in post.likes:
            post.likes.remove(str(id))
            text = 'Unlike'
        else:   
            post.likes.append(str(id))
            text = 'Like'
        post.save()
        
        return JsonResponse({'data':text, 'likes' : len(post.likes)})

def TogglePostSave(request):
    if request.POST:
        x = request.POST
        pid = x.get('pid')
        post = Post.objects.get(id = pid)
        CProfile = Profile.objects.get(user = request.user)
        if str(pid) in CProfile.saved:
            CProfile.saved.remove(str(pid))
            x = post.saved
            post.saved = x - 1
            text = 'Unsave'
        else:   
            CProfile.saved.append(str(pid))
            x = post.saved
            post.saved = x + 1
            text = 'Save'
        post.save()
        CProfile.save()
        return JsonResponse({'data':text})

def PostComment(request):
    if request.POST:
        x = request.POST
        pid = x.get('pid')
        comment = x.get('comment')
        post = Post.objects.get(id = pid)
        CProfile = Profile.objects.get(user = request.user)
        comment = Comment.objects.create(Post = post, User = request.user, content = comment, likes = 0)
        comment.save()
        comments = Comment.objects.filter(Post = post)
        return JsonResponse({'data':comment.content, "clength":len(comments),'comment':comment})

def DeletePost(request):
    if request.POST:
        x = request.POST
        pid = x.get('pid')
        post = Post.objects.get(id = pid)
        postImage = PostImages.objects.filter(Post = post)
        if postImage.exists():
            for i in postImage:
                i.image.delete()
                i.delete()
        post.delete()
        return JsonResponse({'data':'success'})

def ToggleArchivePost(request, pid):
    post = Post.objects.get(id = pid)
    if post.archived:
        post.archived = False
        text = 'Unarchive'
    else:
        post.archived = True
        text = 'Archive'
    post.save()
    return JsonResponse({'data':text})
    


# Story Views
def UploadStory(request):
    if request.POST:    
        image = request.FILES.get('picUpload')
        u = request.user
        type1 = request.POST.get('typeStory')
        type="p"
        if type1 == "on":
            type = "c"
        StoryIns = Story.objects.create(User = u, Image = image, type=type)
        return redirect("Aspirer:Home")

def GetStory(request,id):
    U = User.objects.filter(id = id)[0]
    CProfile = Profile.objects.filter(user= U)[0]
    Stories = Story.objects.filter(User = U)
    x = Stories[0].views
    if x is None:
        x = []
    if str(request.user.id) not in x:
        x.append(str(request.user.id))
        y = Stories[0]
        y.views = x
        y.save()
    UserProfile = Profile.objects.filter(user= request.user)[0]
    t = render_to_string('others/storycaraousel.html',{"stories":Stories,"CProfile":CProfile,"UserProfile":UserProfile})
    return JsonResponse({'data':t})

def DeleteStory1(request):
    if request.POST:
        id = request.POST['id']
        P = Story.objects.get(id = id)
        P.Image.delete()
        P.delete()
    return redirect("Aspirer:Home")


# Chatroo mViews
def Chatroom(request):
    CProfile = Profile.objects.get(user = request.user)
    CUser =   CProfile.user
    SuggestedProfiles = Profile.objects.all()
    suggestions = []
    for i in SuggestedProfiles:
        if (not(i.pvt_acc) or str(i.user.id) in CProfile.followers or str(i.user.id) in CProfile.following):
            suggestions.append(i)
    
    dic = {"title":"ChatRoom", "CProfile":CProfile, "CUser":CUser, "suggestions":suggestions, "active":"chat"}
    return render(request,'chatroom.html', dic)

@csrf_exempt
def OpenChat(request):
    if request.POST:
        User1 = request.POST.get('user1')
        User2 = request.POST.get('user2')
        Users = [int(User1), int(User2)]
        for i in Users:
            c = User.objects.filter(id = i)
        users_len = len(set(Users))
        c = ChatRoom.objects.annotate(
            total_Users=Count('Users'),
            matching_Users=Count('Users', filter=Q(Users__in=Users))
        ).filter(
            matching_Users=users_len,
            total_Users=users_len
        )
        if c.exists():
            c1 = c[0]
        if not c.exists():
            # Create Chatroom Code
            c1 = ChatRoom()
            c1.save()
            for i in Users:
                u = User.objects.get(id = int(i))
                c1.Users.add(u)
            c1.save()
        CProfile = Profile.objects.get(user = request.user)
        SuggestedProfiles = Profile.objects.all()
        CUser = request.user
        suggestions = []
        for i in SuggestedProfiles:
            if (not(i.pvt_acc) or str(i.user.id) in CProfile.followers or str(i.user.id) in CProfile.following):
                suggestions.append(i)

        Chats = ChatMsg.objects.filter(Chatroom = c1)
        f = render_to_string('others/chat.html',{'Chats':Chats,'CUser':CUser})
        return JsonResponse({'data':f, "cid":c1.id,'ChatE':Chats.exists()})        

@csrf_exempt
def SendMessage(request):
    if request.POST:
        content = request.POST.get("content")
        chatroom_id = request.POST.get("chatroom")
        chatroom = ChatRoom.objects.get(id = chatroom_id)
        chat = ChatMsg.objects.create(content = content, Chatroom = chatroom, status = "sending", sender = request.user)
        Chats = ChatMsg.objects.filter(Chatroom = chatroom_id)
        f = render_to_string('others/chat.html',{'Chats':Chats,'CUser':request.user})
        return JsonResponse({'data':f,'ChatE':Chats.exists(), "c_id":chat.id})       

@csrf_exempt
def MessageSent(request):
    if request.POST:
        id = request.POST.get('id')
        Chat = ChatMsg.objects.get(id = id)
        Chat.status = "delivered"
        Chat.save()
        return JsonResponse({"data":True})
