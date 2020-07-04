from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator


from .models import User, Post, UserFollowing, UserLike

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from .pagination import pagination

def index(request):
    context = {}
    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get("content")
        
        if len(content) > 280 or content.strip() == "":
            context['error'] = True
        else:
            user = User.objects.get(username=request.user.username)
            post = Post(user=user, content=content)
            post.save()
    
    posts = Post.objects.all().order_by('-date')
    context['page_obj'] = pagination(request, posts)

    return render(request, "network/index.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def profile(request, username):
    context = {}
    try:
        user = User.objects.get(username=username)
        context['username'] = user.username
        if user.username != request.user.username and request.user.is_authenticated:
            context['followed'] = UserFollowing.objects.filter(user_id=request.user, following_user_id=user).count()
        context['following'] = user.following.all().count()
        context['followers'] = user.followers.all().count()
        
        posts = Post.objects.filter(user=user).order_by('-date')
        context['page_obj'] = pagination(request, posts)
    except:
        context['user'] = False
    return render(request, "network/profile.html", context)

def follow(request, username):
    try:
        follow = User.objects.get(username=username)
        if follow.username != request.user.username and request.user.is_authenticated:
            UserFollowing.objects.create(user_id=request.user, following_user_id=follow)
        return HttpResponseRedirect(reverse("profile", args=[username]))
    except:
        return HttpResponseRedirect(reverse("index"))

def unfollow(request, username):
    try:
        unfollow = User.objects.get(username=username)
        if unfollow.username != request.user.username and request.user.is_authenticated:
            if UserFollowing.objects.filter(user_id=request.user, following_user_id=unfollow).count():
                userFollowing = UserFollowing.objects.get(user_id=request.user, following_user_id=unfollow)
                userFollowing.delete()
        return HttpResponseRedirect(reverse("profile", args=[username]))
    except:
        return HttpResponseRedirect(reverse("index"))

def following(request):
    context = {}
    following = request.user.following.all()
    users = []
    for userFollowing in following:
        users.append(userFollowing.following_user_id)
    
    posts = Post.objects.filter(user__in=users).all().order_by('-date')
    context['page_obj'] = pagination(request, posts)

    return render(request, "network/following.html", context)


def edit_post(request):
    if request.method == "POST":
        content = request.POST.get('content')
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        if post.user.username != request.user.username:
            return render(request, "network/profile.html")
        post.content = content
        post.save()
        return HttpResponse(status=200)
    else:
        return render(request, "network/profile.html")

@csrf_exempt
def likes(request):
    if request.method == "POST" and request.user.is_authenticated:
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        if UserLike.objects.filter(post=post, author=request.user).count():
            like = UserLike.objects.get(post=post, author=request.user)
            like.delete()
            return JsonResponse({"liked":False, "count":post.post_likes.all().count()})
        else:
            like = UserLike(post=post, author=request.user)
            like.save()
            return JsonResponse({"liked":True, "count":post.post_likes.all().count()})
    else:
        return HttpResponseRedirect(reverse("index"))