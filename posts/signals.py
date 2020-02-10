from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from posts.models import Post, FeedPost, PostReaction


@receiver(post_save, sender=Post)
def after_saving_post(sender, instance, created, **kwargs):
    if created:
        followers = list(map(lambda x: x.follower_user, instance.created_by.following_users.all())) + [
            instance.created_by]
        feed_posts = list(map(lambda u: FeedPost(user=u, post=instance), followers))

        FeedPost.objects.bulk_create(feed_posts)

        if instance.parent:
            instance.parent.comments_count = F('comments_count') + 1
            instance.parent.save()


@receiver(post_delete, sender=Post)
def after_deleting_post(sender, instance, **kwargs):
    if instance.parent:
        instance.parent.comments_count = F('comments_count') - 1
        instance.parent.save()


@receiver(post_save, sender=PostReaction)
def after_reacting_to_post(sender, instance, created, **kwargs):
    if created:
        if instance.like:
            instance.post.likes_count = F('likes_count') + 1
        else:
            instance.post.dislikes_count = F('dislikes_count') + 1
        instance.post.save()


@receiver(post_delete, sender=PostReaction)
def after_deleting_reaction(sender, instance, **kwargs):
    if instance.like:
        instance.post.likes_count = F('likes_count') - 1
    else:
        instance.post.dislikes_count = F('dislikes_count') - 1
    instance.post.save()
