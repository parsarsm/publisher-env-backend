from rest_framework import routers

from posts.views import PostsViewSet, ImagesViewSet, ProfileViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='Post')
router.register(r'images', ImagesViewSet, basename='Image')
router.register(r'profiles', ProfileViewSet, basename='Profile')
router.register(r'users', UserViewSet, basename='User')
