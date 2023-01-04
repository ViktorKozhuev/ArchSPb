from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import CreateCommentForm, CreatePostForm
from .models import Post
from users.models import Profile


class Posts(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Статьи'}
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.all()


class ShowPost(DetailView):
    model = Post
    template_name = 'posts/post.html'
    slug_field = "url"
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return Post.objects.get(url=self.kwargs.get("url"))


@login_required
def add_comment(request, pk):
    post_ = Post.objects.get(id=pk)
    if request.method == 'POST':
        post = {
            'user': request.user.id,
            'profile': Profile.objects.get(user_id=request.user.id).id,
            'comment': request.POST['comment'],
            'post': Post.objects.get(id=pk).id
        }

        form = CreateCommentForm(post)
        if request.POST.get("parent", None):
            post['parent'] = int(request.POST.get("parent"))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponse(status=405)
    return HttpResponse(status=500)


@login_required
def add_post(request):

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.profile = Profile.objects.get(user_id=request.user.id)
            post.draft = True
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        form = CreatePostForm()

    context = {
        "form": form,
    }

    return render(request, 'posts/add_post.html', context)


class AddPage(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

