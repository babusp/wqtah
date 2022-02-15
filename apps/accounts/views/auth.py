"""
auth views
"""
# django imports
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework import serializers
from apps.accounts.models.auth import User

# local imports
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE
from apps.utility.viewsets import (
    CustomModelPostViewSet,
    get_object_or_404,
    CustomModelUpdateViewSet,
    CustomModelViewSet,
)
from apps.accounts.serializers.auth import (
    RegisterSerializer,
    SendOtpSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserProfileSerializer,
    UpdatePasswordSerializer,
    ForgotSendOtpSerializer,
    ForgotPasswordSerializer,
)
from apps.utility.common import CustomResponse, Response

USER = get_user_model()


# Create your views here.


class LoginViewSet(CustomModelPostViewSet):
    """
    used to login the user and return the token info
        POST  /login/
        request body: {"email": "example@email.com", "password": "my-password"}
        content-type: Application/json
    """

    serializer_class = LoginSerializer

    def create(self, request):
        """login create override"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return CustomResponse(
                status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
            ).success_response(data=serializer.data["data"])
        return CustomResponse(
            status=status.HTTP_400_BAD_REQUEST, detail=ERROR_CODE["4002"]
        ).error_message(error=serializer.errors)


class RegistrationViewSet(CustomModelPostViewSet):
    """View set class to register user"""

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2001"]
        ).success_response(data=serializer.data)


class SendOTPViewSet(CustomModelPostViewSet):
    """View set class to change password"""

    serializer_class = SendOtpSerializer

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return CustomResponse(
            status=200, detail=SUCCESS_CODE["2005"]
        ).success_response()


class ProfileViewSet(CustomModelViewSet):
    """ViewSet class for profile"""

    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    queryset = USER.objects.all()
    http_method_names = ("get", "patch")

    def get_queryset(self):
        """Return profile related to user only"""
        queryset = self.queryset
        if self.request.user.id:
            return queryset.filter(id=self.request.user.id)
        return queryset

    def get_object(self):
        """
        return requested user
        """
        user_id = self.kwargs.get("pk")
        user_obj = get_object_or_404(USER, id=user_id)
        return user_obj

    def partial_update(self, request, *args, **kwargs):
        """
        Override  method to pass current request to the serializer
        :param request:  wsgi request
        :param args:  list
        :param kwargs: dict
        :return: Json Response
        """
        instance = self.get_object()
        serializer = self.serializer_class(
            instance,
            data=request.data,
            partial=True,
            context={"user": self.request.user},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2007"]
        ).success_response(serializer.data)


class LogoutView(generics.GenericAPIView):
    """User Logout"""

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = RegisterSerializer

    def post(self, request):
        """User Logout validate"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2004"]
        ).success_response(data=serializer.data)


class UpdatePasswordViewSet(CustomModelUpdateViewSet):
    """ViewSet class for profile"""

    serializer_class = UpdatePasswordSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()


class ForgotSendOTPViewSet(CustomModelPostViewSet):
    """View set class to send otp to when forgot password"""

    serializer_class = ForgotSendOtpSerializer


class ForgotPasswordViewSet(CustomModelPostViewSet):
    serializer_class = ForgotPasswordSerializer
