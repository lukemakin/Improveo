from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views import View
from .models import ProblemPost, GeneralPost, Like, Post
from profiles.models import Profile
from .forms import PostForm, CommentForm, ExampleForm
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FormUserRequiredMixin, FormUserOwnerMixin
# Create your views here.


class PostExampleView(View):
    form_class = ExampleForm
    initial = {'name': 'example of name'}
    template_name = 'posts/example.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:post-list")
        return render(request, self.template_name, {'form': form})


class GeneralPostDelete(LoginRequiredMixin, DeleteView):
    model = GeneralPost
    template_name = 'posts/confirm.html'
    success_url = reverse_lazy("posts:post-list")

    def get_object(self, *args, **kwargs):
        obj = super(GeneralPostDelete, self).get_object()
        if not obj.author.user == self.request.user:
            raise ValueError("You have to be the owner of this post to delete it")
        return obj


class GeneralPostUpdateView(LoginRequiredMixin, FormUserOwnerMixin, UpdateView):
    form_class = PostForm
    model = GeneralPost
    template_name = 'posts/update.html'
    success_url = '/board/'


class GeneralDetailPost(LoginRequiredMixin, DetailView):
    model = GeneralPost
    template_name = 'posts/detail.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post_ = get_object_or_404(GeneralPost, pk=pk)
        return post_

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post_ = self.get_object()
        form = CommentForm(self.request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            profile = Profile.objects.get(user=self.request.user)
            instance.user = profile
            instance.post = post_
            instance.body = form.cleaned_data.get('body')
            form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class ProblemDetailPost(LoginRequiredMixin, DetailView):
    model = ProblemPost
    template_name = 'posts/detail.html'
    pk_url_kwarg = 'pk1'
    login_url = reverse_lazy('account_login')


class PostCreateView(FormUserRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/board.html'
    success_url = reverse_lazy('posts:post-list')
    login_url = reverse_lazy('account_login')

    def get_context_data(self, *args, **kwargs):
        qs1 = ProblemPost.objects.public_only()
        qs2 = GeneralPost.objects.all()
        qs = sorted(chain(qs1, qs2), reverse=True,
                    key=lambda obj: obj.timestamp)
        context = super().get_context_data(*args, **kwargs)
        context["object_list"] = qs
        return context


@login_required
def like_post(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        post_id = request.POST.get('post_id')

        post_obj = Post.objects.get(id=post_id)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

    like, created = Like.objects.get_or_create(
        user=profile, post_id=post_id)

    if not created:
        if like.value == 'Like':
            like.value = 'Unlike'
        else:
            like.value = 'Like'

    like.save()
    return redirect('posts:post-list')
