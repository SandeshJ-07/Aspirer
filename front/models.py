from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListCharField
from PIL import Image
import datetime

# Profile Model
class Profile(models.Model):
    # Choices
    gender_chocies = (
        ('M',"Male"),
        ("F","Female"),
        ("N","Prefer Not To Say")
    )


    # Fields
    user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True)
    username = models.CharField(null=False, default = " ", max_length = 20)
    ProfileImg = models.ImageField(null=True,upload_to="images/profile_pic/",default="media/images/profile_pic/default.png")
    contact = models.CharField(max_length = 10)
    Email = models.EmailField(null=False)
    address = models.CharField(null = False, max_length = 50,blank = True)
    website = models.CharField(null=True,blank=True, max_length=30, default="")
    gender = models.CharField(max_length=1,choices = gender_chocies, default = "N")
    pvt_acc = models.BooleanField(default=False)
    activity_status = models.BooleanField(null=False, default = False)
    story_share = models.BooleanField(null=False, default = False)
    close_friends = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    hide_story = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    blocked_users = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    restricted_users = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    followers =  ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    following =  ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ] ,
        null = True,
        blank = True
    )
    saved =  ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    follow_request =  ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    bio = models.CharField(max_length = 100,default=" ", blank=True)

    def __str__(self):
        return self.user.username

# Posts Related Models
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete= models.CASCADE)
    uploadTime = models.DateTimeField(default= datetime.datetime.now())
    likes =  ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        default = [ ],
        null = True,
        blank = True
    )
    caption = models.CharField(null=False,max_length=300)
    shares = models.IntegerField(default=0)
    saved = models.IntegerField(default=0)
    allow_comments = models.BooleanField(default=True)
    comments = ListCharField(
        base_field=models.CharField(max_length = 10),
        size= 6,
        max_length = (6 * 11),
        default = [],
        null = True,
        blank = True,
    )
    Showimage = models.ImageField(null=False, blank=False, upload_to="images/posts/", default = " ")
    archived = models.BooleanField(null=False, default = False)
    mentions = ListCharField(
        base_field=models.CharField(max_length=50),
        size=6,
        max_length=(6 * 51),  # 6 * 10 character nominals, plus commas
        null = True,
        blank = True
    )
    Location = models.CharField(blank=True, null=True,max_length=50)

class PostImages(models.Model):
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/posts/")

class Comment(models.Model):
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=50, null=True,blank = False)
    reply_to = models.CharField(max_length = 100, null=True, blank= True)
    uploadTime = models.DateTimeField(default= datetime.datetime.now())
    likes = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6, 
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        null = True,
        blank = True
    )
    replies = ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        null = True,
        blank = True
    )


story_type = (
    ("p","public"),
    ("c","close_friends")
)

class Story(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadTime = models.DateTimeField(default= datetime.datetime.now())
    type = models.CharField(max_length=20,choices=story_type,default="p")
    Image = models.ImageField(upload_to="images/stories/", null=False, blank = False)
    views =  ListCharField(
        base_field=models.CharField(max_length=10),
        size=6,
        default = [],
        max_length=(6 * 11),  # 6 * 10 character nominals, plus commas
        null = True,
        blank = True
    )
    shares = models.IntegerField(default = 0)

# Chatroom Models
Msgstatus =(
    ('seen','seen'),
    ('delivered','delivered'),
    ('sending','sending')
)

class ChatRoom(models.Model):
    Users = models.ManyToManyField(User)
    name = models.CharField(max_length  = 25, default =" Chatroom", blank=False)

class ChatMsg(models.Model):
    Chatroom = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length = 10 , choices=Msgstatus, default="sending")
    sendTime = models.DateTimeField(default= datetime.datetime.now())
    content = models.TextField(null=False, blank=False, max_length=6000)