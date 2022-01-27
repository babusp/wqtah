"""
auth serializer file
"""
# django imports
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

# local imports
from apps.accounts.messages import ERROR_CODE, SUCCESS_CODE

from apps.accounts.models.auth import (User, UserPhoneVerification)
from apps.accounts.managers import UserManager

from apps.accounts.tasks.auth import send_sms_otp_task

USER = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    """ used to verify the login credentials and return the login response """

    email_or_phoneNo = serializers.CharField(max_length=100)

    class Meta:
        """ meta class """
        model = User
        fields = ('email_or_phoneNo', 'password')

    def validate_username(self, email_or_phoneNo):
        user = User.objects.filter((Q(email__iexact=email_or_phoneNo, is_active=False).first() | Q(
            phone_no__iexact=email_or_phoneNo, is_active=False).first()))

        if user:
            user = user[0]
            serializer = SendPhoneOTPSerializer(data={'email': user.email_or_phoneNo,
                                                'phone_no': user.email_or_phoneNo},
                                                context={'user': user, 'request': self.context['request']})
            if serializer.is_valid():
                serializer.save()
            raise serializers.ValidationError({'detail': ERROR_CODE['4008']})
        return user

    def validate(self, attrs):
        """ used to validate the email/phoneNo and password """

        user = User.objects.filter(email__iexact=attrs['email_or_phoneNo']).first() \
               or User.objects.filter(phone_no__iexact=attrs['email_or_phoneNo']).first()

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

        return {'token': instance.get_token(), 'id': instance.id, 'first_name': instance.first_name,
                'last_name': instance.last_name, 'phone_no': instance.phone_no, 'email': instance.email,
                'role': instance.role
                }


class RegisterSerializer(serializers.ModelSerializer):
    """ used to register the user """

    class Meta:
        """ meta class """
        model = USER
        fields = ('first_name', 'last_name', 'country_code', 'phone_no', 'password')

    def validate(self, attrs):
        """ used to validate the data"""
        user = USER.objects.filter(phone_no__iexact=attrs['phone_no']).first()
        if user:
            raise serializers.ValidationError({'detail': ERROR_CODE['4004']})
        return attrs

    def create(self, validated_data):
        """ used to return the user object """
        user = USER.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        """ used to return the user json """
        return {'detail': SUCCESS_CODE['2001'], 'token': instance.get_token()}


class SendPhoneOTPSerializer(serializers.ModelSerializer):
    """
    Send phone OTP serializers
    """
    class Meta(object):
        """ Meta information """
        model = UserPhoneVerification
        fields = ('id', 'country_code', 'phone_no')

    def validate(self, attrs):
        attrs.update({'user': self.context['user']})
        return attrs

    def create(self, validated_data):
        user = self.context['user']
        validated_data['otp'] = UserPhoneVerification.generate_otp()
        validated_data['expired_at'] = datetime.now() + timedelta(minutes=500)

        # Deactivate all previous otp generated for the new phone
        user.phone_verification_set.update(is_active=False)
        instance = super(SendPhoneOTPSerializer, self).create(validated_data)
        return instance

    def save(self, send_otp=True, **kwargs):
        instance = super(SendPhoneOTPSerializer, self).save(**kwargs)
        if send_otp:
            send_sms_otp_task(instance)
        return instance
