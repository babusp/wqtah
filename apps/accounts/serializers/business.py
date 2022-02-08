from rest_framework import serializers
from apps.accounts.models import BusinessDetail


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = "__all__"
