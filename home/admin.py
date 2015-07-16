from django.contrib import admin
from home import models


class PostAdmin(admin.ModelAdmin):
    pass


class UserViewedPostAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.UserViewedPost, UserViewedPostAdmin)
