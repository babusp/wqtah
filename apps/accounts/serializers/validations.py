from django.db.models import Q

from apps.accounts.messages import ERROR_CODE
from apps.accounts.serializers.verifivations import SendEmailVerificationLinkSerializer
from rest_framework import serializers
from apps.accounts.models.auth import User


class ValidateUser:
    email_or_phoneNo = serializers.CharField(max_length=170, required=False)

    def validate_username(self, email_or_phoneNo):
        # user = User.objects.filter(username=username, is_active=False)
        user = User.objects.filter((Q(email__iexact=email_or_phoneNo, is_active=False).first() | Q(
            phone_no__iexact=email_or_phoneNo, is_active=False).first()))

        if user:
            user = user[0]
            serializer = SendEmailVerificationLinkSerializer(
                data={'email': user.email_or_phoneNo, 'phone_no': user.email_or_phoneNo},
                context={'user': user, 'request': self.context['request']})
            if serializer.is_valid():
                serializer.save()
            raise serializers.ValidationError(
                'Sorry! Your account is not active. We have sent you a verification link to activate your account.')
        return user

    def validate(self, attrs):
        """ used to validate the email/phoneNo and password """
        # s = attrs['email_or_phoneNo']
        # print(s)
        # user = User.objects.filter(email__iexact=attrs['email_or_phoneNo']).first() \
        #        or User.objects.filter(phone_no__iexact=attrs['email_or_phoneNo']).first()

        user = User.objects.filter((Q(email__iexact=attrs['email_or_phoneNo']) | Q(
            phone_no__iexact=attrs['email_or_phoneNo'])))

        # user = UserManager.validate_email_mobile_login(self, attrs['email_or_phoneNo'])
        # print("inside login ser validate.................", user)

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


# email_or_phoneNo = serializers.CharField(max_length=170, required=False)


def validate_username(self):
    email_or_phoneNo = serializers.CharField(max_length=170, required=False)

    user = User.objects.filter(email__iexact=email_or_phoneNo, is_active=False).first() or User.objects.filter(
        phone_no__iexact=email_or_phoneNo, is_active=False).first()
    print("user inside validators.py..........", user)

    if user:
        user = user[0]
        serializer = SendEmailVerificationLinkSerializer(
            data={'email': user.email_or_phoneNo, 'phone_no': user.email_or_phoneNo},
            context={'user': user, 'request': self.context['request']})
        if serializer.is_valid():
            serializer.save()
        raise serializers.ValidationError(
            'Sorry! Your account is not active. We have sent you a verification link to activate your account.')
    return user




