from django.db import models
from django.db.models import permalink

# Create your models here.

import datetime
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    image = models.FileField(null=True, blank=True)
    email = models.EmailField(max_length=255)
    author = models.CharField(max_length=255, null=True)

    posted = models.DateTimeField(db_index=True, auto_now_add=True)

    category = models.ForeignKey('BestBoards.Category')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, {'slug': self.slug})

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.posted <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, {'slug': self.slug})