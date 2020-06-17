from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.shortcuts import redirect
from . import forms
from django.contrib.auth.decorators import login_required


def index(request):
    latest = Post.objects.order_by('-pub_date')[:11]
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            return redirect('/')
        return render(request, 'new.html', {'form': form})
    form = forms.PostForm()
    return render(request, 'new.html', {'form': form})
