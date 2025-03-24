from django.db import models
from blog.models import Post
from django.urls import reverse


class Comment(models.Model):
    """Model representing a comment on a blog post."""
    RECOMMEND_CHOICE = (
        ('yes', 'I recommend this post'),
        ('no', "I don't recommend this post"),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recommend = models.CharField(max_length=3, choices=RECOMMEND_CHOICE)
    approved = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the comment."""
        return f'{self.email}-{self.post.title}'

    def get_absolute_url(self):
        """Return the absolute URL for the comment detail view."""
        return reverse("comment:comment_detail", kwargs={"pk": self.pk})

    def get_snippet(self):
        return ' ' .join(self.message.split()[:10]) + '...'
