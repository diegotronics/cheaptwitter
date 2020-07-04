from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=280)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.content}. Likes: {self.likes}"

class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class UserLike(models.Model):
    author = models.ForeignKey(User, related_name="like_authors", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)