from django.contrib.auth.models import User
from django.db import models


class Timestamp(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Profile(Timestamp):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    fb_id = models.CharField(max_length=255, blank=True)
    profile_pic = models.CharField(max_length=255, blank=True)
    locale = models.CharField(max_length=48, blank=True)
    timezone = models.IntegerField(default='+7')
    location = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    score = models.IntegerField(default=100)
    bio = models.CharField(max_length=255, blank=True)
    email_confirmed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'common_profile'


class CelebModel(Timestamp):
    name = models.CharField(max_length=255)
    ig_handle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    followers = models.IntegerField(default=0)
    profile_pic = models.CharField(max_length=255, blank=True)
    score = models.IntegerField(default=0)
    last_scraped = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'influencers_celebrity'
