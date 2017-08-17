# -*- coding: utf-8 -*-
#import files
from __future__ import unicode_literals
from django.db import models
import uuid
from django.db import IntegrityError
#create usermodel to form a table with the help of django
class UserModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

def __str__(self):
      return self.name

#create login model
class login(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

#create session token
class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()

class PostModel(models.Model):
    user = models.ForeignKey(UserModel)
    image= models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    has_liked = models.BooleanField(default=False)
    caption = models.CharField(max_length=240,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('-created_on')

class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    upvote_number = models.IntegerField(default=0)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)




