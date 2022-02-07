""" utility models """
from django.db import models
from apps.utility.constants import IMAGE, VIDEO
# Create your models here.


class BaseModel(models.Model):
    """Base model for create data and update date"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Base Meta class"""
        abstract = True


class Attachments(BaseModel):
    """
    create table Attachments
    """
    MEDIA_TYPE = (
        (IMAGE, 'image'),
        (VIDEO, 'video'),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(max_length=2, blank=True, null=True, choices=MEDIA_TYPE)
    file = models.FileField(blank=True, null=True, upload_to='post_attachments')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='post_attachments_thumbnail')
    height = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)

    class Meta:
        """Base Meta class"""
        abstract = True
