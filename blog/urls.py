from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterFormView.as_view(), name="register"),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/create/', views.create_post, name='create-post'),
    path('mycomments/', views.MyCommentView.as_view(), name='my-comments'),
    path('comment/create/<int:pk>', views.comment_create, name='create-comment'),
]
