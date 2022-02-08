"""
auth serializer file
"""
# django imports
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# local imports
from apps.accounts.messages import ERROR_CODE

from apps.accounts.models.auth import User
from apps.services.twilio_services import send_twilio_otp, verify_twilio_otp

USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    """used to verify the login credentials and return the login response"""

    email_or_phoneNo = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    data = serializers.JSONField(read_only=True)

    def validate(self, data):
        phone = data.get("email_or_phoneNo")
        password = data.get("password")
        try:
            user = User.objects.get(phone_no=phone)
            if phone and password:
                verified = user.check_password(password)
                if verified:
                    data["data"] = UserWithTokenSerializer(user).data
                    return data
            raise serializers.ValidationError(ERROR_CODE["4003"])
        except User.DoesNotExist:
            raise serializers.ValidationError(ERROR_CODE["4001"])

    def create(self, validated_data):
        """overriding create"""
        phone = (validated_data["phone_no"],)
        try:
            user = User.objects.get(phone_no=phone)
        except Exception:
            raise serializers.ValidationError(ERROR_CODE["4001"])
        return user


class UserBasicInfoSerializer(serializers.ModelSerializer):
    """Base class for user profile"""

    class Meta:
        """
        Meta class defining user model and including field
        """

        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "country_code",
            "phone_no",
            "otp_verified",
            "role",
        ]


class UserWithTokenSerializer(UserBasicInfoSerializer):
    """Return user token along with data"""

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

        fields = UserBasicInfoSerializer.Meta.fields + ["token"]


class RegisterSerializer(serializers.ModelSerializer):
    """used to register the user"""

    class Meta:
        model = USER
        fields = (
            "first_name",
            "last_name",
            "email",
            "country_code",
            "phone_no",
            "password",
            "otp",
        )

    def to_representation(self, instance):
        """override to return user serialized data"""
        return UserWithTokenSerializer(instance).data

    def create(self, validated_data):
        """overriding create"""
        try:
            response = verify_twilio_otp(
                validated_data["country_code"],
                validated_data["phone_no"],
                validated_data["otp"],
            )
        except Exception:
            raise serializers.ValidationError(ERROR_CODE["4009"])
        if response == "approved":
            instance = User.objects.create_user(**validated_data)
            instance.otp_verified = True
            instance.save()
            return instance


class SendOtpSerializer(serializers.Serializer):
    """used to send otp to user phone no"""

    country_code = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)

    class Meta:
        fields = ("country_code", "phone_no")

    def create(self, validated_data):
        """overriding create serializer"""
        try:
            send_twilio_otp(
                validated_data["country_code"], validated_data["phone_no"], "sms"
            )
        except Exception as e:
            raise serializers.ValidationError(ERROR_CODE["4010"])
        return validated_data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            return ERROR_CODE["4011"]
