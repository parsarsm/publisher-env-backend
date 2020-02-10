from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post, PostReaction, Profile, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
    def to_representation(self, instance):
        user = UserSerializer(instance).data

        profile = {}
        if instance.profile.all():
            profile = ProfileSerializer(instance.profile.all()[0]).data

        return {**profile, **user}


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
