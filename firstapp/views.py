from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from firstapp.models import Post
from django.views.generic import (
ListView,DetailView,CreateView,DeleteView,UpdateView
)
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/home.html'
    ordering = ['-date_posted']

    paginate_by = '10'



class PostCreateView(CreateView):
    model = Post
    fields = ['title','content','image']
    context_object_name = 'form'
    template_name = 'blog/post_form.html'

    # for getting author id by method overriding from the CreateView
    def form_valid(self, form):
        form.instance.author =self.request.user # getting author id by the session data
        return super().form_valid(form)



from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','image']
    context_object_name = 'form'
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return  super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

    def handle_no_permission(self):
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name()
        )




class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_delete_form.html'
    success_url = reverse_lazy ('home')

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

    def handle_no_permission(self):
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name()
        )

class UserPostDetails(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/home.html'
    ordering = ['-date_posted']

    def get_queryset(self):
        user= get_object_or_404(User,username=self.kwargs['username'])
        return Post.objects.filter(author=user).order_by('-date_posted')




