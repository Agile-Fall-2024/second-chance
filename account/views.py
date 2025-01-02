from django.contrib.auth import authenticate, login, logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, AccountSerializer
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.models import User
from .translations import translate


class SignupView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: translate("Bad Request"),
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description=translate("Username")),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description=translate("Password")),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description=translate("OTP sent"),
                examples={
                    "application/json": {
                        "message": translate("OTP sent to your email address. Please verify OTP to proceed.")
                    }
                },
            ),
            400: translate("Bad Request"),
            401: translate("Unauthorized"),
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': translate("Please provide both username and password.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            account = user.account
            otp = account.generate_otp()
            send_mail(
                translate("Ciz-Miz Login OTP"),
                translate("Your OTP for login is: %(otp)s", otp=otp),
                'chizmiz.agile@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response(
                {'message': translate("OTP sent to your email address. Please verify OTP to proceed.")},
                status=status.HTTP_200_OK
            )
        return Response({'error': translate("Invalid credentials")}, status=status.HTTP_401_UNAUTHORIZED)


class OTPVerificationView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description=translate("Username")),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description=translate("OTP")),
            },
            required=['username', 'otp']
        ),
        responses={
            200: openapi.Response(description=translate("Login successful")),
            400: translate("Invalid or expired OTP"),
            404: translate("User not found"),
        }
    )
    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')

        if not username or not otp:
            return Response(
                {'error': translate("Please provide both username and OTP.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
            account = user.account
            if account.otp == otp and account.otp_expiry > now():
                login(request, user)
                account.otp = None
                account.otp_expiry = None
                account.save()
                return Response({'message': translate("Login successful")}, status=status.HTTP_200_OK)
            else:
                return Response({'error': translate("Invalid or expired OTP.")}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': translate("User not found.")}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(description=translate("Logout successful")),
        }
    )
    def post(self, request):
        logout(request)
        return Response({'message': translate("Logout successful")}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: UserSerializer,
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AccountUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AccountSerializer,
        responses={
            200: AccountSerializer,
            400: translate("Bad Request"),
        }
    )
    def put(self, request):
        account = request.user.account
        data = request.data
        serializer = AccountSerializer(account, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)