from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth import get_user_model
from django.conf import settings

from django.contrib.postgres.fields import JSONField

from django.db.models.signals import post_save
from django.dispatch import receiver


class Timestamp(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Profile(Timestamp):

    USER_GENDER_CHOICES = (
        ("None", "None selected"),
        ("Male", "Male"),
        ("Female", "Female"),
        ("Not_of_this_earth", "Not of this Earth"),
        ("Nunna_yo_biznizz", "Nunna yo biznizz!"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    fb_id = models.CharField(max_length=255, blank=True)
    profile_pic = models.CharField(max_length=255, blank=True)
    locale = models.CharField(max_length=48, blank=True)
    timezone = models.IntegerField(default='+8')
    location = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    score = models.IntegerField(default=0)
    bio = models.CharField(max_length=255, blank=True)
    email_confirmed = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=128,
        blank=True,
        default='None',
        choices=USER_GENDER_CHOICES,
    )

    class Meta:
        managed = False
        db_table = 'common_profile'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    print("POST SAVE", sender, instance, created)
    print("POST SAVE KWARGS", kwargs)
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()


class CelebModel(Timestamp):
    name = models.CharField(max_length=255)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='linked_profile'
    )
    ig_handle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    followers = models.IntegerField(default=0)
    profile_pic = models.CharField(max_length=255, blank=True)
    score = models.IntegerField(default=0)
    tag_list = JSONField(blank=True, null=True)
    interests_list = JSONField(blank=True, null=True)
    concepts_list = JSONField(blank=True, null=True)
    word_set = JSONField(blank=True, null=True)
    last_scraped = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'influencers_celebrity'
