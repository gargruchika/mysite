# -*- coding: utf-8 -*-
#different import files
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm,UpvoteForm,SearchForm
from models import UserModel , SessionToken , PostModel ,login, LikeModel,CommentModel
from imgurpython import ImgurClient
from django.http import HttpResponse,HttpResponseForbidden
from datetime import timedelta,datetime
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import logout
import os
from clarifai.rest import Image as CImage
from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='cc38356c59fe4e11bcf1f7a9decea234')
model = app.models.get('apparel')
image = CImage(url='https://samples.clarifai.com/apparel.jpeg')
model.predict([image])
imgs=app.inputs.search_by_predicted_concepts(concept='apparel')
print imgs
import sendgrid
from sendgrid.helpers.mail import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_ID =  '54ceade8d449315'
CLIENT_SECRET = 'a2f439835e340c444f786a6c99fef14bded5e177'
SENDGRID_API_KEY ='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'

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
              sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)                                #email send for verification.
              from_email = Email("ruchikagarg764@example.com.")
              to_email = Email(email)
              subject = "Successfully signed up."
              content = Content("text/plain", "welcome to smart p2p marketplace! enjoy your app")
              mail = Mail(from_email, subject, to_email, content)
              response = sg.client.mail.send.post(request_body=mail.get())
              if response.status_code == 202:
                  messages.warning(request, "Email Send :)")
                  return render(request,'success.html')
              else:
                messages.warning(request, "Unable to send Email! :(")
                return render(request, 'index.html')
            else:
                messages.warning(request,'user name and password in not long enough!')
                return render(request,'index.html')
        else:
             messages.warning(request,"please fill all the fields correctly!")
             form = SignUpForm()
    else:
        form = SignUpForm()
    return render(request, 'index.html', {'time': datetime.now(),},{'form': form})

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
                    messages.warning(request, "Incorrect Password! Please try agaim!")
    elif request.method == "GET":
        form = LoginForm()
    response_data['form'] = form
    return render(request,'login.html', response_data)

#post view for posts
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
            messages.warning(request, "Post should not be created successfully.")
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')


#feed view to show the feed/result
def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like=LikeModel.objects.filter(post_id=post.id,user=user).first()
            if existing_like:
                post.has_liked = True
            messages.warning(request, "Post should be created successfully.")
        return render(request,'feed.html',{'posts':posts})
    else:
        return redirect('/login/')

#like view for liking posts by user
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like =LikeModel.objects.filter(post_id=post_id,user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id,user=user)
                messages.warning(request, "Like should be created successfully.")
                postget=PostModel.objects.filter(id=post_id).first()                         #email send for verification
                userid=postget.user_id
                user=UserModel.objects.filter(id=userid).first()
                email=user.email
                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
                from_email = Email("ruchikagarg764@example.com.")
                to_email = Email(email)
                subject = "someone liked your post!"
                content = Content("text/plain", "post should be liked")
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
            else:
                existing_like.delete()
            return redirect ('/feed/')
    else:
        return redirect('/login/')

#comment view for comments on post
def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user,post_id=post_id,comment_text=comment_text)
            comment.save()
            messages.warning(request, "comment should be created successfully.")
            postget = PostModel.objects.filter(id=post_id).first()                                     #email send for verification
            userid = postget.user_id
            user = UserModel.objects.filter(id=userid).first()
            email = user.email
            sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
            from_email = Email("ruchikagarg764@example.com.")
            to_email = Email(email)
            subject = "someone should comment on your post!"
            content = Content("text/plain", "comment should be posted by someone")
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
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

#for logout the current account
def logout_view(request):
    user = check_validation(request)
    if user is not None:
        new_session = SessionToken.objects.filter(user=user).last()
        if new_session:
            new_session.delete()
    return render(request,'logout.html')

#for upvoting the comments
def upvote_view(request):
    user = check_validation(request)
    comment =None
    print "upvote view"
    if user and request.method == 'POST':
        form = UpvoteForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            comment_id = int(form.cleaned_data.get('id'))
            comment = CommentModel.objects.filter(id=comment_id).first()
            print "Not upvoted yet"
            if comment is not None:
                print "Upvoted"
                comment.upvote_number += 1
                comment.save()
                print comment.upvote_number
                messages.success(request, "Wow!comment Sucessfully upvoted!")
                return redirect('/feed/')
            else:
                print "some error"
                messages.success(request, "some error")
                return redirect('/feed/')
        else:
            messages.warning(request, "Error:comment not be upvoted!try again")
            return redirect('/feed/')
    else:
        messages.warning(request, "Error:Please fill Login details first!")
        return redirect('/login/')

#search view for searching the post particular by user name
def search_view(request):
    user = check_validation(request)
    if user:
        if request.method == "GET":
            search_form = SearchForm(request.GET)
            if search_form.is_valid():
                print 'valid search'
                username_query = search_form.cleaned_data.get('search_query')
                print username_query
                user_with_query = UserModel.objects.filter(username=username_query).first();
                posts = PostModel.objects.filter(user=user_with_query)
                return render(request, 'feed.html', {'posts': posts})
            else:
                return redirect('/feed/')
    else:
        return redirect('/login/')

#concept of clarifai
def get_relevant_tags(image_url):
    response_data = app.tag_urls([image_url])
    tag_urls = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tag_urls.append(concept['name'])

    return tag_urls