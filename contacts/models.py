from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=200, blank=True, null=True)
  bio = models.CharField(max_length=500, blank=True, null=True)
  facebook = models.URLField(max_length=200, blank=True, null=True)
  linkedin = models.URLField(max_length=200, blank=True, null=True)
  phone = models.BigIntegerField(null=True)
  email = models.CharField(max_length=200, blank=True, null=True)
  spotify = models.CharField(max_length=200, blank=True, null=True)
  soundcloud = models.URLField(max_length=200, blank=True, null=True)
  snapchat = models.CharField(max_length=200, blank=True, null=True)
  snapcode = models.ImageField(null=True)
  twitter = models.CharField(max_length=200, blank=True, null=True)
  instagram = models.CharField(max_length=200, blank=True, null=True)