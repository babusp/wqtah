"""
auth views
"""
# django imports
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# local imports
from apps.accounts.messages import SUCCESS_CODE
from apps.accounts.models import User
from apps.accounts.serializers.auth import RegisterSerializer, SendOtpSerializer
from apps.utility.viewsets import CustomModelPostViewSet
from apps.utility.common import CustomResponse

USER = get_user_model()


# Create your views here.


class LoginView(APIView):
    """
    used to login the user and return the token info
        POST  /login/
        request body: {"email": "example@email.com", "password": "my-password"}
        content-type: Application/json
    """

    def post(self, request):
        phone = request.data.get("phone_no")
        password = request.data.get("password")
        try:
            user = User.objects.get(phone_no=phone)
        except User.DoesNotExist:
            return Response({"error": "please check authentication credentils"})

        # check user is authenticater or not
        verified = user.check_password(password)
        if verified:
            jwt_token = user.get_token()
            return Response(jwt_token)
        else:
            return Response({"error": "please check authentication credentils"})


class RegistrationViewSet(CustomModelPostViewSet):
    """ View set class to register user """
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """ overriding for custom response """
        serializer = super(RegistrationViewSet, self).create(request, *args, **kwargs)
        return CustomResponse(status=status.HTTP_200_OK, detail=SUCCESS_CODE['2001']).success_response(data=serializer.data)


class VerifyOTPEndpoint(APIView):
    """ Verify OTP """

    def post(self, request):
        """ post request of otp verification"""
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
            return Response({"message": "opt not verified"}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPViewSet(CustomModelPostViewSet):
    """ View set class to change password """
    serializer_class = SendOtpSerializer

    def create(self, request, *args, **kwargs):
        """ overriding for custom response """
        super(SendOTPViewSet, self).create(request, *args, **kwargs)
        return CustomResponse(status=200, detail=SUCCESS_CODE['2005']).success_response()
