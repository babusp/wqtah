"""
auth serializer file
"""
# django imports
from django.contrib.auth import get_user_model
from rest_framework import serializers

# local imports
from apps.accounts.messages import ERROR_CODE, SUCCESS_CODE
from apps.accounts.models.auth import (UserPhoneVerification, UserEmailVerification)


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


class RegisterSerializer(serializers.ModelSerializer):
    """ used to register the user """

    class Meta:
        """ meta class """
        model = USER
        fields = ('first_name', 'last_name', 'country_code', 'phone_no', 'email', 'password')

    def validate(self, attrs):
        """ used to validate the data"""
        user = USER.objects.filter(email__iexact=attrs['email']).first()
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
        return {'detail': SUCCESS_CODE['2001']}


class LogoutSerializer(serializers.Serializer):
    """
    used to logout the user
    """
    registration_id = serializers.CharField(max_length=250, required=False)

    class Meta:
        """
        meta class
        """
        fields = ('registration_id', )


class SendPhoneOTPSerializer(serializers.ModelSerializer):
    """
    Send phone OTP serializers
    """
    class Meta(object):
        """ Meta information """
        model = UserPhoneVerification
        fields = ('id', 'country_code', 'phone')

    def validate(self, attrs):
        attrs.update({'user': self.context['user']})
        return attrs

    def create(self, validated_data):
        user = self.context['user']
        validated_data['otp'] = UserPhoneVerification.generate_otp()
        validated_data['expired_at'] = datetime.now() + timedelta(minutes=OTP_EXPIRY_TIME)

        # Deactivate all previous otp generated for the new phone
        user.phone_verification_set.update(is_active=False)
        instance = super(SendPhoneOTPSerializer, self).create(validated_data)
        return instance

    def save(self, send_otp=True, **kwargs):
        instance = super(SendPhoneOTPSerializer, self).save(**kwargs)
        if send_otp:
            send_sms_otp_task(instance)
        return instance


class ValidatePhoneOTPSerializer(serializers.ModelSerializer):
    """
    Validate phone OTP serializers
    """
    class Meta(object):
        """ Meta information """
        model = UserPhoneVerification
        fields = ('otp', )

    def validate_otp(self, value):
        if datetime.now() > self.instance.expired_at:
            raise serializers.ValidationError('OTP expired.')
        if value == self.instance.otp:
            return value
        raise serializers.ValidationError('Incorrect OTP.')

    def update(self, instance, validated_data):
        instance.is_active = False
        instance.is_verified = True
        instance.save()

        # Save user profile
        profile = UserProfile.objects.filter(user=instance.user)
        profile = profile[0] if profile else UserProfile()
        profile.user = instance.user
        profile.country_code = instance.country_code
        profile.phone = instance.phone
        profile.save()
        return profile


class SendEmailOTPSerializer(serializers.ModelSerializer):
    """
    Send email OTP serializers
    """
    class Meta(object):
        """ Meta information """
        model = UserEmailVerification
        fields = ('id', 'email')

    @staticmethod
    def validate_email(value):
        value = value.strip().lower()
        if User.objects.filter(Q(email__iexact=value) | Q(username__iexact=value)).exists():
            raise serializers.ValidationError('Email is already in use.')
        return value

    def validate(self, attrs):
        attrs.update({'user': self.context['user']})
        return attrs

    def create(self, validated_data):
        validated_data['otp'] = UserEmailVerification.generate_otp()
        validated_data['expired_at'] = datetime.now() + timedelta(minutes=OTP_EXPIRY_TIME)
        UserEmailVerification.objects.filter(email=validated_data.get('email')).update(
            is_active=False)
        instance = super(SendEmailOTPSerializer, self).create(validated_data)
        # execute_task(send_email_otp_task, instance, async=False)
        return instance

    def save(self, **kwargs):
        instance = super(SendEmailOTPSerializer, self).save(**kwargs)
        send_email_otp_task(instance)
        return instance


class ValidateEmailOTPSerializer(serializers.ModelSerializer):
    """
    Send email OTP serializers
    """
    otp = serializers.CharField()

    class Meta(object):
        """ Meta information """
        model = UserEmailVerification
        fields = ('otp',)

    def validate_otp(self, value):
        if datetime.now() > self.instance.expired_at:
            raise serializers.ValidationError('OTP expired.')
        if value == self.instance.otp:
            return value
        raise serializers.ValidationError('Incorrect OTP.')

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.is_active = False
            instance.is_verified = True
            instance.save()
            # Save email in user
            user = instance.user
            user.email = instance.email
            user.username = instance.email
            user.save()
            return user


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


class ValidateEmailVerificationLinkSerializer(serializers.ModelSerializer):
    """
    Send email OTP serializers
    """

    class Meta(object):
        """ Meta information """
        model = UserEmailVerification
        fields = ('otp',)

    def validate_otp(self, value):
        if value == self.instance.otp:
            return value
        raise serializers.ValidationError('Incorrect OTP.')

    def update(self, instance, validated_data):
        instance.is_active = False
        instance.save()
        # Mark user as active
        user = instance.user
        user.is_active = True
        user.save()
        return user


# class UserDetailSerializer(serializers.ModelSerializer):
#     """ used to serialize the user model """
#
#     class Meta:
#         model = USER
#         fields = ('id', 'first_name', 'last_name', 'profile_picture')


# class ForgotPasswordSerializer(serializers.Serializer):
#     """
#     forgot password serializer.
#     """
#     email = serializers.CharField(required=True)
#
#     def validate(self, attrs):
#         """
#         :param attrs: data to be validated
#         """
#         user_obj = USER.objects.filter(email__iexact=attrs['email']).first()
#         if not user_obj:
#             raise serializers.ValidationError({"detail": ERROR_CODE['4001']})
#         if not user_obj.is_verified:
#             raise serializers.ValidationError({"detail": ERROR_CODE["4005"]})
#         if not user_obj.is_active:
#             raise serializers.ValidationError({"detail": ERROR_CODE["4003"]})
#
#         self.context.update({'user': user_obj})
#         return attrs
#
#     def create(self, validated_data):
#         """ send forgot password link """
#         user = self.context['user']
#         user.send_forgot_pass_mail()
#         return user
#
#     def to_representation(self, instance):
#         """ string representation """
#         return {'detail': SUCCESS_CODE}
