"""
auth serializer file
"""
# django imports
from wsgiref import validate
from xml.dom.minidom import Attr
from xml.sax.xmlreader import AttributesImpl
from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from apps.utility.common import Response
from django.core.mail import send_mail


# local imports
from apps.accounts.messages import ERROR_CODE, SUCCESS_CODE
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

    country_code = serializers.CharField(
        required=True, allow_blank=False, allow_null=False
    )
    phone_no = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        """
        Meta class defining user model and including field
        """

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

    def validate(self, attrs):
        """validating phone no"""
        user = User.objects.filter(phone_no=attrs["phone_no"]).first()
        if user:
            raise serializers.ValidationError(ERROR_CODE["4004"])
        return attrs

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
            if response == "approved":
                instance = User.objects.create_user(**validated_data)
                instance.otp_verified = True
                instance.save()
                return instance
        except Exception:
            raise serializers.ValidationError(ERROR_CODE["4009"])


class SendOtpSerializer(serializers.Serializer):
    """used to send otp to user phone no"""

    country_code = serializers.CharField(
        required=True, allow_blank=False, allow_null=False
    )
    phone_no = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    class Meta:
        """
        Meta class defining login fields
        """

        fields = ("country_code", "phone_no")

    def validate(self, attrs):
        """validating phone no"""
        user = User.objects.filter(phone_no=attrs["phone_no"]).first()
        if user:
            raise serializers.ValidationError(ERROR_CODE["4004"])
        return attrs

    def create(self, validated_data):
        """overriding create serializer"""
        try:
            send_twilio_otp(
                validated_data["country_code"], validated_data["phone_no"], "sms"
            )
        except Exception:
            raise serializers.ValidationError(ERROR_CODE["4010"])
        return validated_data


class UserProfileSerializer(serializers.ModelSerializer):
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
        ]


class LogoutSerializer(serializers.Serializer):
    """User LogoutSerializer"""

    refresh = serializers.CharField()

    def validate(self, attrs):
        """User LogoutSerializer"""
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        """User Logout Exception handling"""
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError(ERROR_CODE["4011"])


##### Update Password
class UpdatePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password", "confirm_password")

    def to_representation(self, instance):
        """override to return user response"""
        return {"message": "password updated successfully"}

    def update(self, instance, validate_data):
        old_password = validate_data.get("old_password")
        new_password = validate_data.get("new_password")
        confirm_password = validate_data.get("confirm_password")
        if not instance.check_password(old_password):
            raise serializers.ValidationError("old_passwrord not match")
        if new_password == confirm_password:
            # updating new password
            instance.set_password(new_password)
            instance.save()
            send_mail(
                "PASSWORD UPDATED",
                "password changed successfully",
                "psobhan777@gmail.com",
                [instance.email],
                fail_silently=False,
            )
            return instance
        else:
            raise serializers.ValidationError(
                "new_password, confirm_password not match"
            )


# forgot password


class ForgotPasswordSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(write_only=True, required=True)
    otp = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("otp", "new_password", "confirm_password")

    # def to_representation(self, instance):
    #     """override to return user serialized data"""
    #     return UserWithTokenSerializer(instance).data

    def create(self, attrs, validated_data):
        """overriding create"""
        user = User.objects.filter(phone_no=attrs["phone_no"]).first()
        if user:
            try:
                response = verify_twilio_otp(
                    validated_data["country_code"],
                    validated_data["phone_no"],
                    validated_data["otp"],
                )
                if response == "approved":
                    new_password = validated_data.get("new_password")
                    confirm_password = validated_data.get("confirm_password")
                    if new_password == confirm_password:
                        # updating new password
                        instance.save()
                        instance.otp_verified = True
                    send_mail(
                        "PASSWORD UPDATED",
                        "password changed successfully",
                        "psobhan777@gmail.com",
                        [instance.email],
                        fail_silently=False,
                    )
                    return instance

            except Exception:
                raise serializers.ValidationError(ERROR_CODE["4009"])
        else:
            raise serializers.ValidationError(ERROR_CODE["4001"])


class ForgotSendOtpSerializer(serializers.Serializer):
    """used to send otp to user phone no"""


otp = serializers.CharField(write_only=True, required=True)
new_password = serializers.CharField(write_only=True, required=True)
confirm_password = serializers.CharField(write_only=True, required=True)


class Meta:
    model = User
    fields = ("otp", "new_password", "confirm_password")


# def to_representation(self, instance):
#     """override to return user serialized data"""
#     return UserWithTokenSerializer(instance).data


def create(self, attrs, validated_data):
    """overriding create"""
    user = User.objects.filter(phone_no=attrs["phone_no"]).first()
    if user:
        try:
            response = verify_twilio_otp(
                validated_data["country_code"],
                validated_data["phone_no"],
                validated_data["otp"],
            )
            if response == "approved":
                instance = User.objects.create_user(**validated_data)
                instance.otp_verified = True
                new_password = validated_data.get("new_password")
                confirm_password = validated_data.get("confirm_password")

                if new_password == confirm_password:
                    # updating new password
                    instance.set_password(new_password).save()
                send_mail(
                    "PASSWORD UPDATED",
                    "password changed successfully",
                    "psobhan777@gmail.com",
                    [instance.email],
                    fail_silently=False,
                )
                return instance

        except Exception:
            raise serializers.ValidationError(ERROR_CODE["4009"])
    else:
        raise serializers.ValidationError(ERROR_CODE["4001"])
