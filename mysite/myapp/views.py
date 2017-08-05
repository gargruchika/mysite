# -*- coding: utf-8 -*-
#different import files
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm,UpvotingForm
from models import UserModel , SessionToken , PostModel ,login, LikeModel,CommentModel,UpvotingModel
from imgurpython import ImgurClient
from django.http import HttpResponse
from datetime import timedelta,datetime
from django.utils import timezone
from django.contrib.auth import logout
import os
import sendgrid
from sendgrid.helpers.mail import *
from django.contrib.auth.hashers import make_password,check_password
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_ID =  '54ceade8d449315'
CLIENT_SECRET = 'a2f439835e340c444f786a6c99fef14bded5e177'
SENDGRID_API_KEY='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'
# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to database
            empty=len(username)==None and len(password)==None
            if len(username)>=4 and len(password)>=3:
              user = UserModel(name=name, password=make_password(password), email=email, username=username)
              user.save()
              sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
              from_email = Email("ruchikagarg764@example.com.")
              to_email = Email(email)
              subject = "Successfully signed up."
              content = Content("text/plain", "welcome to instaclone! enjoy your app")
              mail = Mail(from_email, subject, to_email, content)
              response = sg.client.mail.send.post(request_body=mail.get())
              return redirect('/login/')
              if response.status_code == 202:
               message = "Email Send! :)"
              else:
                message = "Unable to send Email! :("
                return render(request, 'success.html', {'response': message})
            else:
                text ={}
                text = 'user name and password in not long enough!'
                return render(request,'index.html',{'text':text})
        else:
             form = SignUpForm()
    elif request.method == "GET":
        form = SignUpForm()
        today = datetime.now()
        return render(request, 'index.html', {'today': today, 'form': form})

#for login the page
def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():                                      #check the valid form.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()
            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'
    elif request.method == "GET":
        form = LoginForm()
    response_data['form'] = form
    return render(request,'login.html', response_data)

def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR +"/"+ post.image.url)

                client = ImgurClient(CLIENT_ID,CLIENT_SECRET)
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')



def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like=LikeModel.objects.filter(post_id=post.id,user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request,'feed.html',{'posts':posts})
    else:
        return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like =LikeModel.objects.filter(post_id=post_id,user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id,user=user)
            else:
                existing_like.delete()
            return redirect ('/feed/')
    else:
        return redirect('/login/')

def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user,post_id=post_id,comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
             return session.user
    else:
        return None

def logout_view(request):
     return render(request,'logout.html')

def upvoting_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':

        form = UpvotingForm(request.POST)
        if form.is_valid():
            response_data = {}
            comment_id = form.cleaned_data.get('comment')
            upvoted = UpvotingModel.objects.filter(comment_id=comment_id,user=user).first()

            if not upvoted:
                UpvotingModel.objects.create(comment=comment_id,user=user)
                response_data['subject']='upvoted'
                response_data['content']='comment upvoted by:'+form.cleaned_data.get('comment').user.name

            else:
                upvoted.delete()
                response_data['subject']='downvoted'
                response_data['content']='comment downvoted by:'+form.cleaned_data.get('comment').user.name

            return redirect('/feed/')
    else:
        return redirect('/login/')