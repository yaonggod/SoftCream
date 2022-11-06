from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category_followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='category_followings')
    def __str__(self):
      return self.name

class Articles(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_articles')

class Comment(models.Model):
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    articles = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Photo(models.Model):
    post = models.ForeignKey(Articles, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

class Image(models.Model):
    articles = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='articles_image')
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    image_thumbnail = ImageSpecField(source='image',
                                processors=[ResizeToFill(200, 200)],
                                format='JPEG',
                                options={'quality': 60})
