from django.contrib import admin

from posts.models import Post, ProfileMembership, PostReaction, Profile, Image


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(PostReaction)
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(ProfileMembership)
