from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post, PostReaction


class PostSerializer(serializers.ModelSerializer):
    liked = serializers.IntegerField(read_only=True)
    disliked = serializers.IntegerField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'summary', 'created_at', 'updated_at', 'likes_count', 'dislikes_count',
                  'comments_count', 'liked', 'disliked', 'parent', 'created_by', 'channel']


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        exclude = ['id']
