# -*- coding: utf-8 -*-
#import files
from __future__ import unicode_literals
from django.db import models
import uuid

#create usermodel to form a table with the help of django
class UserModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    #phone_num = models.CharField(max_length=31)
    #age = models.IntegerField(default=0)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    #has_verified_mobile = models.BooleanField(default=False)

def __str__(self):
    return self.name + '' + self.email

#create login model
class login(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=10)
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