"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#import files
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from myapp.views import signup_view, feed_view ,login_view

# different urls for different pages.
urlpatterns = [
    url(r'^admin/', admin.site.urls),       #url for  admin page.
    url('feed/', feed_view),                #url for feed page.
    url('login/', login_view),              #url for directly login the page if the user has already signup.
    url('',signup_view)                     #url for new signup if the new user wants to create an account.


]