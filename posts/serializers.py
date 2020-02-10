from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post, PostReaction, Profile, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    avatar_file = serializers.SerializerMethodField(method_name='get_avatar', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def get_avatar(self, instance):
        return instance.avatar.file.url

    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'birthday', 'description', 'avatar_file']


class UserWithProfileSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        pass

    def to_representation(self, instance):
        user = UserSerializer(instance).data

        profile = {}
        if instance.profile.all():
            profile = ProfileSerializer(instance.profile.all()[0]).data

        return {**profile, **user}

    @staticmethod
    def _split_data(d):
        pass

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'file']


class PostSerializer(serializers.ModelSerializer):
    liked = serializers.IntegerField(read_only=True)
    disliked = serializers.IntegerField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        return UserWithProfileSerializer(instance.created_by).data

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'summary', 'created_at', 'updated_at', 'likes_count', 'dislikes_count',
                  'comments_count', 'liked', 'disliked', 'parent', 'created_by', 'channel', 'user']


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        exclude = ['id']
