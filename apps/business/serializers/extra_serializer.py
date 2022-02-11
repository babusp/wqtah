""" business extra serializers """
from rest_framework import serializers

from apps.business.choices import MEDIA_TYPE
from apps.business.models.business import BusinessProfileMediaMapping, BusinessProfile


class BusinessProfileAttachmentListSerializer(serializers.ModelSerializer):
    """ Business profile media serializer"""
    class Meta:
        """ meta class """
        model = BusinessProfileMediaMapping
        fields = "__all__"


class AddBusinessProfileAttachmentSerializer(serializers.ModelSerializer):
    """ AddAttachmentSerializer class for adding attachments to post """

    business_profile = serializers.SlugRelatedField(queryset=BusinessProfile.objects.all(), slug_field='id')
    file_type = serializers.ChoiceField(choices=MEDIA_TYPE, required=True)
    file = serializers.FileField(required=True)

    class Meta:
        """
        Meta class defining user post model and including field
        """
        model = BusinessProfileMediaMapping
        fields = ['id', 'file', 'file_type', 'business_profile', 'name']
