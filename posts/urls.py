from rest_framework import routers

from posts.views import PostsViewSet, ImagesViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='Post')
router.register(r'images', ImagesViewSet, basename='Image')
