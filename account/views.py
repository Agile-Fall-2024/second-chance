from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, AccountSerializer
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.models import User


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate OTP and send to email
            account = user.account
            otp = account.generate_otp()
            send_mail(
                'Ciz-Miz Login OTP',
                f'Your OTP for login is: {otp}',
                'chizmiz.agile@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response(
                {'message': 'OTP sent to your email address. Please verify OTP to proceed.'},
                status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class OTPVerificationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')

        if not username or not otp:
            return Response(
                {'error': 'Please provide both username and OTP.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
            account = user.account
            if account.otp == otp and account.otp_expiry > now():
                # OTP is valid
                login(request, user)
                account.otp = None  # Clear OTP after use
                account.otp_expiry = None
                account.save()
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AccountUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        account = request.user.account
        data = request.data
        serializer = AccountSerializer(account, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
