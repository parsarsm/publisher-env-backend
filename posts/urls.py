from rest_framework import routers

from posts.views import PostsViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='Post')
