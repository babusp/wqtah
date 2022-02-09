from rest_framework import serializers
from apps.accounts.models import StaffDetail


class StaffSerilizer(serializers.ModelSerializer):

    assigned_business = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StaffDetail
        fields = "__all__"
