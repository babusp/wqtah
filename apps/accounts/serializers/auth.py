"""
auth serializer file
"""
# django imports
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# local imports
from apps.accounts.messages import ERROR_CODE, SUCCESS_CODE
from apps.accounts.models.auth import User
from apps.services.twilio_services import send_twilio_otp, verify_twilio_otp
from apps.services.sendgrid import send_email

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
    business_profile = serializers.SerializerMethodField()

    def get_business_profile(self, obj):
        """ business detail """
        business_profile = obj.businessprofile_set.last()
        if business_profile:
            return {"level": business_profile.level, "is_admin_verified": business_profile.is_admin_verified,
                    'id': business_profile.id}
        return None

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
            "business_profile"
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

    country_code = serializers.CharField(required=True, allow_blank=False, allow_null=False)
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
        extra_kwargs = {'first_name': {"allow_blank": False},
                        'last_name': {"allow_blank": False},
                        'email': {"allow_blank": False, "required": True},
                        'phone_no': {"allow_blank": False},
                        'country_code': {"allow_blank": False}}


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
        return {"message": SUCCESS_CODE["2003"]}

    def update(self, instance, validate_data):
        old_password = validate_data.get("old_password")
        new_password = validate_data.get("new_password")
        confirm_password = validate_data.get("confirm_password")
        if not instance.check_password(old_password):
            raise serializers.ValidationError(ERROR_CODE["4002"])
        if new_password != confirm_password:
            raise serializers.ValidationError(ERROR_CODE["4006"])
        # updating new password
        instance.set_password(new_password)
        instance.save()
        send_email(instance.email)
        return instance


# forgot password


class ForgotPasswordSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(write_only=True, required=True)
    phone_no = serializers.CharField(write_only=True, required=True)
    otp = serializers.IntegerField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "country_code",
            "phone_no",
            "otp",
            "new_password",
            "confirm_password",
        )

    def to_representation(self, instance):
        """override to return user response"""
        return {"message": SUCCESS_CODE["2003"]}

    def create(self, validated_data):
        """overriding create"""
        user = User.objects.filter(phone_no=validated_data["phone_no"]).first()

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
                        user.set_password(new_password)
                        user.otp_verified = True
                        user.save()
                        send_email(user.email)
                        return user
                else:
                    raise serializers.ValidationError(ERROR_CODE["4009"])
            except Exception as e:
                raise serializers.ValidationError(str(e))
        else:
            raise serializers.ValidationError(ERROR_CODE["4001"])


class ForgotSendOtpSerializer(serializers.Serializer):
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

    def create(self, validated_data):
        """validating phone no"""
        user = User.objects.filter(phone_no=validated_data["phone_no"]).first()
        if user:
            try:
                send_twilio_otp(
                    validated_data["country_code"],
                    validated_data["phone_no"],
                    "sms",
                )
            except Exception:
                raise serializers.ValidationError(ERROR_CODE["4001"])
        return validated_data
