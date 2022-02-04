"""
auth views
"""
# django imports
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView


# local imports
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE
from apps.accounts.models import User
from apps.accounts.serializers.auth import (
    RegisterSerializer,
    SendOtpSerializer,
    LoginSerializer,
)
from apps.utility.viewsets import CustomModelPostViewSet
from apps.utility.common import CustomResponse

USER = get_user_model()


# Create your views here.


class LoginView(RetrieveAPIView):
    """
    used to login the user and return the token info
        POST  /login/
        request body: {"email": "example@email.com", "password": "my-password"}
        content-type: Application/json
    """

    serializer_class = LoginSerializer

    def post(self, request):
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
        return CustomResponse(
                status=status.HTTP_200_OK, detail=SUCCESS_CODE["2001"]
            ).success_response(data=serializer.data["data"])


class VerifyOTPEndpoint(APIView):
    """Verify OTP"""

    def post(self, request):
        """post request of otp verification"""
        phone = request.data.get("phone_no")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(phone_no=phone)
        except User.DoesNotExist:
            return Response({"error": "please check authentication credentils"})

        # check otp is valid or not
        if user and user.otp == otp:
            return Response({"message": "opt verified"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "opt not verified"}, status=status.HTTP_400_BAD_REQUEST
            )


class SendOTPViewSet(CustomModelPostViewSet):
    """View set class to change password"""

    serializer_class = SendOtpSerializer

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        super(SendOTPViewSet, self).create(request, *args, **kwargs)
        return CustomResponse(
            status=200, detail=SUCCESS_CODE["2005"]
        ).success_response()
