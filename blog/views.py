from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CommentCreate, PostCreate, RegisterForm
from .models import Comment, Post


def index(request):

    num_posts = Post.objects.count()
    num_comments = Comment.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_posts': num_posts, 'num_comments': num_comments,
                 'num_visits': num_visits},
    )


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class PostListView(generic.ListView):
    model = Post
    paginate_by = 20
    template_name = 'post_list.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostCreate(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                brief_description = form.cleaned_data['brief_description']
                full_description = form.cleaned_data['full_description']
                posted = form.cleaned_data['posted']
                author = request.user
                post = Post.objects.create(title=title, brief_description=brief_description,
                                           full_description=full_description,
                                           posted=posted, author=author)
                post.save()
        else:
            form = PostCreate()
        return render(request, 'create_post.html', {'form': form})
    return HttpResponseRedirect('')


class MyCommentView(LoginRequiredMixin, generic.ListView):

    model = Comment
    template_name = 'my_comments.html'
    paginate_by = 10

    def get_queryset(self):
        return Comment.objects.filter(username=self.request.user).filter(posted_com=True)


def comment_create(request,):
    if request.method == 'POST':
        form = CommentCreate(request.POST)
        username = request.user
        if form.is_valid():
            text = form.cleaned_data['text']
            Comment.objects.create(username=username, text=text)
            return HttpResponseRedirect(reverse_lazy(''))
    else:
        form = CommentCreate()
    return render(request, 'create_comment.html', {'form': form, })
