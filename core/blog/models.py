from django.db import models
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (
        ('drf', 'Draft'),
        ('pub', 'Published'),
    )
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    counted_views = models.IntegerField(default=0)
    category = models.ManyToManyField('Category')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})
    
    def increment_counted_views(self):
        self.counted_views += 1
        self.save()
    

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

