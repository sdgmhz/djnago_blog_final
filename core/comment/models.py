from django.db import models
from blog.models import Post


class Comment(models.Model):
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
        return f'{self.email}-{self.post.title}'
