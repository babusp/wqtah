"""
auth views
"""
# django imports
from django.contrib.auth import get_user_model
from rest_framework import status, permissions

# local imports
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE
from apps.accounts.models import User
from apps.accounts.serializers.auth import (RegisterSerializer, SendOtpSerializer, LoginSerializer,
                                            UserProfileSerializer)
from apps.utility.viewsets import CustomModelPostViewSet, get_object_or_404, CustomModelViewSet
from apps.utility.common import CustomResponse

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
        """ overriding for custom response """
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
    """ ViewSet class for profile """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'patch')

    def get_queryset(self):
        """ Return profile related to user only """
        if self.request.user.id:
            return self.request.user

    def get_object(self):
        """
        return request user
        """
        user_id = self.kwargs.get('pk')
        user_obj = get_object_or_404(User, id=user_id)
        return user_obj

