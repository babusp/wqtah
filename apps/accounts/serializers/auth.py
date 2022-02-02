"""
auth serializer file
"""
# django imports
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

# local imports
from apps.accounts.messages import ERROR_CODE

from apps.accounts.models.auth import User
from apps.services.twilio_services import send_twilio_otp, verify_twilio_otp

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


class UserBasicInfoSerializer(serializers.ModelSerializer):
    """ Base class for user profile """

    class Meta:
        """
        Meta class defining user model and including field
        """
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'country_code', 'phone_no', 'otp_verified', 'role']


class UserWithTokenSerializer(UserBasicInfoSerializer):
    """ Return user token along with data"""
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(obj):
        """
        login token for that user
        """
        return obj.get_token()

    class Meta(UserBasicInfoSerializer.Meta):
        """
        Meta class
        """
        fields = UserBasicInfoSerializer.Meta.fields + ['token']


class RegisterSerializer(serializers.ModelSerializer):
    """ used to register the user """

    class Meta:
        model = USER
        fields = ('first_name', 'last_name', "email", 'country_code', 'phone_no', 'password', 'otp')

    def to_representation(self, instance):
        """ override to return user serialized data """
        return UserWithTokenSerializer(instance).data

    def create(self, validated_data):
        """ overriding create """
        try:
            response = verify_twilio_otp(validated_data["country_code"], validated_data['phone_no'],
                                         validated_data['otp'])
        except Exception:
            raise serializers.ValidationError(ERROR_CODE['4009'])
        if response == "approved":
            instance = User.objects.create_user(**validated_data)
            instance.otp_verified = True
            instance.save()
            return instance



class SendOtpSerializer(serializers.Serializer):
    """ used to send otp to user phone no"""
    country_code = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)

    class Meta:
        fields = ('country_code', 'phone_no')

    def create(self, validated_data):
        """overriding create serializer"""
        send_twilio_otp(validated_data["country_code"], validated_data['phone_no'], 'sms')
        return validated_data
