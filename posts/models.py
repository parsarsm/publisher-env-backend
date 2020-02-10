from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q


class Channel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    rules = models.TextField()
    created_at = models.DateTimeField(auto_created=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ChannelMembership(models.Model):
    class ChannelMembershipRoles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        EDITOR = 'EDITOR', 'Editor'
        MEMBER = 'MEMBER', 'Member'

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, db_index=True)
    role = models.CharField(choices=ChannelMembershipRoles.choices, max_length=10, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_memberships')


class ProfileMembership(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_users')
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_users')
    created_at = models.DateTimeField(auto_created=True, db_index=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True)
    dislikes_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    def get_user_view(user_id=None):
        if user_id:
            return Post.objects.annotate(
                liked=Count('postreaction', filter=Q(postreaction__user=user_id, postreaction__like=True)),
                disliked=Count('postreaction', filter=Q(postreaction__user=user_id, postreaction__like=False))
            )
        else:
            return Post.objects.annotate(
                liked=0,
                disliked=0
            )


class FeedPost(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_index=True, null=False)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, db_index=True, null=False, related_name="feed")


class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField()

    class Meta:
        unique_together = ['post', 'user']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    metadata = models.TextField()
    created_at = models.DateTimeField(auto_created=True, db_index=True)


class Image(models.Model):
    file = models.FileField(blank=False, null=False)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE, db_index=True, unique=True,
                             related_name='profile')
    avatar = models.ForeignKey(to=Image, null=True, blank=True, on_delete=models.SET_NULL)
    birthday = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, default='')
