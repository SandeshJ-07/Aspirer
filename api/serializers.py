from django.db import models
from front.models import *
from django.contrib.auth.models import User
from rest_framework import serializers
# Create your models here.

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'