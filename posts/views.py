from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from posts.models import Post, PostReaction, Image
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer, PostReactionSerializer, ImageSerializer, UserWithProfileSerializer


def paginate_queryset(queryset, request, key, page_size):
    pager_from = request.query_params.get('_from')
    pager_to = request.query_params.get('_to')

    query = dict()
    if pager_from is not None:
        query['{key}__gt'.format(key=key)] = pager_from
    if pager_to is not None:
        query['{key}__lt'.format(key=key)] = pager_to

    if len(query):
        queryset = queryset.filter(**query)

    queryset = queryset.order_by('-{pk}'.format(pk=key))

    if pager_from:
        return queryset
    else:
        return queryset[:page_size]


class LikeDislikeViewSet:
    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        return self._reaction(request, pk, True)

    @action(detail=True, methods=['post'])
    def hi(self, request, pk=None):
        return Response(UserWithProfileSerializer(User.objects.get(pk=pk)).data)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        return self._reaction(request, pk, False)

    def _reaction(self, request, pk, like):
        if request.method == 'DELETE':
            PostReaction.objects.filter(user=request.user.id, post=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            data = {
                'post': pk,
                'user': request.user.id,
                'like': like
            }
            serializer = PostReactionSerializer(data=data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class PostsViewSet(ViewSet, LikeDislikeViewSet):
    page_size = 20

    @action(detail=False)
    def latest(self, request):
        posts = paginate_queryset(
            Post.get_user_view(request.user.id).filter(parent=None),
            request,
            'id',
            self.page_size
        )

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def hottest(self, request):
        posts = Post.get_user_view(request.user.id) \
            .filter(parent=None, created_at__gte=datetime.today() - timedelta(days=1)) \
            .order_by('-likes_count')

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def list(self, request):
        posts = paginate_queryset(
            Post.get_user_view(request.user.id).filter(parent=None, feed__user=request.user),
            request,
            'id',
            self.page_size
        )

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        PostReaction.objects.filter(user=request.user.id, post=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        post = Post.get_user_view(request.user.id).get(pk=pk)
        replies = Post.get_user_view(request.user.id).filter(
            Q(parent=pk) | Q(parent__parent=pk) | Q(parent__parent=pk))
        serializer = PostSerializer([post] + list(replies), many=True)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ImagesViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

# class ProfileViewSet(ViewSet):
#     def retrieve(self, request, pk=None):
#         post = Post.get_user_view(request.user.id).get(pk=pk)
#         replies = Post.get_user_view(request.user.id).filter(
#             Q(parent=pk) | Q(parent__parent=pk) | Q(parent__parent=pk))
#         serializer = PostSerializer([post] + list(replies), many=True)
#         return Response(serializer.data)
#
#     def update(self, request, pk, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = get_object_or_404(Post, pk=pk)
#         serializer = PostSerializer(instance, data=request.data, partial=partial)
#         try:
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValidationError as e:
#             return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
#
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return self.update(request, *args, **kwargs)
