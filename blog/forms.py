from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostCreate(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'brief_description', 'full_description', 'posted']


class CommentCreate(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'posted_com']
