from django.contrib import admin

from posts.models import Post, ProfileMembership, PostReaction


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(PostReaction)
admin.site.register(ProfileMembership)
