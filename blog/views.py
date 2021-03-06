from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from .models import Post, SiteSettings
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post()
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.objects.get()
        return context


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        site_settings = SiteSettings.objects.get()
        comments = post.comments.filter(approved=True).order_by('created_at')
        tags = post.tags.all()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'site_settings': site_settings,
                'comments': comments,
                "commented": False,
                'tags': tags,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        site_settings = SiteSettings.objects.get()
        comments = post.comments.filter(approved=True).order_by("-created_at")

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(
                request,
                'Your comment has been created! It will appear once\
                it is approved!')
            return redirect(reverse('post_detail', kwargs={'slug': slug}))

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                'site_settings': site_settings,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
            },
        )
