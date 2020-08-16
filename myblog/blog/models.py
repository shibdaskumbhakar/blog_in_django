from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.contrib.auth.models import User
# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    slug = models.SlugField(blank=True, unique=True)
    description = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='blog/images', null=True, blank=True)
    views = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return "/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title


def blog_pre_save_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(blog_pre_save_reciver, sender=Blog)


class Like(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)
    likes = models.BooleanField(default=False)
    dislikes = models.BooleanField(default=False)
    blog_title = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
