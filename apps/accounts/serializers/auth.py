"""
auth serializer file
"""
# django imports
from django.contrib.auth import get_user_model
from rest_framework import serializers

# local imports
from apps.accounts.messages import ERROR_CODE, SUCCESS_CODE


USER = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    """ used to verify the login credentials and return the login response """
    email = serializers.EmailField(max_length=100)

    class Meta:
        """ meta class """
        model = USER
        fields = ('email', 'password')

    def validate(self, attrs):
        """ used to validate the email and password """
        user = USER.objects.filter(email__iexact=attrs['email']).first()
        if not user:
            raise serializers.ValidationError({'detail': ERROR_CODE['4001']})
        if not user.is_active:
            raise serializers.ValidationError({'detail': ERROR_CODE['4003']})
        if not user.is_verified:
            raise serializers.ValidationError({'detail': ERROR_CODE['4005']})
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({'detail': ERROR_CODE['4002']})
        self.context.update({'user': user})
        return attrs

    def create(self, validated_data):
        """ used to return the user object """
        return self.context['user']

    def to_representation(self, instance):
        """ used to return the user json """
        return {'token': instance.get_token(), 'id': instance.id}
