from django.contrib.auth.models import User
from django.db import models


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
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_users')
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_users')
    created_at = models.DateTimeField(auto_created=True, db_index=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_created=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    metadata = models.TextField()
    created_at = models.DateTimeField(auto_created=True, db_index=True)
