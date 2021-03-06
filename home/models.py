from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """Stores information about a given post"""

    # User must be set
    user = models.ForeignKey(User, related_name='post_set', blank=False, null=False)
    # Date is set automatically on object creation
    when_posted = models.DateTimeField(auto_now_add=True)
    # Enforce the presence of a caption
    caption = models.TextField(blank=False, null=False)
    # TODO: Actually use this - allow blanks for now
    image = models.ImageField(blank=True, null=True)

    def viewed_by(self, user):
        try:
            self.viewed_post_set.get(user=user)
            return True
        except UserViewedPost.DoesNotExist:
            return False

    def __unicode__(self):
        return '{0} - {1}'.format(self.user.username, self.when_posted)

    class Meta:
        # Default is to order newest -> oldest
        ordering = ['-when_posted']


class UserViewedPost(models.Model):
    """Presence of a row in this table indicates that a
    user has already seen a given post
    """

    user = models.ForeignKey(User, related_name='viewed_post_set')
    post = models.ForeignKey(Post, related_name='viewed_post_set')

    class Meta:
        unique_together = ('user', 'post',)
