from datetime import datetime, timedelta

from django.conf import settings
from rest_framework import serializers

from apps.accounts.models import User, UserEmailVerification


class SendEmailVerificationLinkSerializer(serializers.ModelSerializer):
    """
    Send email OTP serializers
    """
    class Meta(object):
        """ Meta information """
        model = UserEmailVerification
        fields = ('id', 'email')

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get('email'))
        if not user:
            raise serializers.ValidationError('User not found.')
        attrs.update({'user': user[0]})
        return attrs

    @staticmethod
    def get_domain():
        protocol = settings.SERVER_PROTOCOL
        host = settings.SERVER_HOST
        return '{protocol}://{host}/verify-email/'.format(protocol=protocol, host=host)

    def create(self, validated_data):
        validated_data['domain'] = self.get_domain()
        validated_data['expired_at'] = datetime.now() + timedelta(minutes=USER_ACTIVATION_LINK_EXPIRY_TIME)
        validated_data['token'] = UserEmailVerification.generate_token()

        UserEmailVerification.objects.filter(email=validated_data.get('email')).update(
            is_active=False)
        instance = super(SendEmailVerificationLinkSerializer, self).create(validated_data)
        send_email_verification_task({'id': instance.id,
                                      'domain': instance.domain,
                                      'token': instance.token,
                                      'email': instance.user.email,
                                      'first_name': instance.user.first_name})
        return instance