#import files
from django import forms
from models import UserModel,login,PostModel,LikeModel,CommentModel

#forms for signup and login
class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email','username','name','password']

#forms for login
class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']

#forms for post
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image', 'caption']

#forms for like
class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']

#forms for comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text','post','id']

#forms for upvoting
class UpvoteForm(forms.Form):
    id = forms.IntegerField()

#forms for search query
class SearchForm(forms.Form):
    search_query = forms.CharField();


