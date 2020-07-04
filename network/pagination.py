from django.core import serializers
from .models import Post, UserLike

from django.core.paginator import Paginator

def pagination(request, posts):
    posts_list = []
    for post in posts:
        count = post.post_likes.all().count()
        if request.user.is_authenticated:
            liked = (UserLike.objects.filter(post=post, author=request.user).count() == True)
        else:
            liked = False
        post_list = list(Post.objects.filter(id=post.id).values())
        post_list[0]['likes'] = {"count": count, "liked": liked}
        post_list[0]['username'] = post.user.username
        posts_list.append(post_list[0])
    
    posts = posts_list
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj