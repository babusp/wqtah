"""
auth views
"""
# django imports
from django.contrib.auth import get_user_model, logout

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# local imports
from apps.accounts.forms.reset_password import ResetPasswordForm
from apps.accounts.models import User
from apps.accounts.serializers.auth import LoginSerializer, RegisterSerializer
from apps.services.sms_services import send_sms


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


class RegisterView(APIView):
    """
    used to register the user and return the token info
    POST  /signup/
        request body: {
                          "first_name": "string",
                          "email": "user@example.com",
                          "password": "string"
                        }
        content-type: Application/json
    """

    def post(self, request):
        import random

        phone = request.data.get("phone_no")
        password = request.data.get("password")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # send otp
            otp = "".join([str(random.randrange(9)) for _ in range(4)])
            send_sms(phone, otp)

            # new user
            user = serializer.save()
            user.set_password(password)
            user.otp = otp
            user.save()
            return Response(
                {"messsge": "otp send to your mobile number"},
                status=status.HTTP_201_CREATED,
            )

class VerifyOTPEndpoint(APIView):
    def post(self,request):
        phone = request.data.get("phone_no")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(phone_no=phone)
        except User.DoesNotExist:
            return Response({"error": "please check authentication credentils"})

        
        # check otp is valid or not
        if user and user.otp == otp:
            return Response({"message":"opt verified"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"opt not verified"}, status=status.HTTP_400_BAD_REQUEST)

