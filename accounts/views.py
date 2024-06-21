from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer, ProfileSerializer
from .models import User, Profile
from .utils import get_tokens_for_user, send_verification_email



class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user)
            return Response({"message": "User registered successfully. Please check your email to verify your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, uid, token, format=None):
        try:
            u_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=u_id)
        except:
            user = None
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email successfully verified'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data['email_or_phone']
            password = serializer.validated_data['password']
            user = User.objects.filter(email=email_or_phone).first() or User.objects.filter(phone=email_or_phone).first()
            if user and user.check_password(password):
                token = get_tokens_for_user(user)
                return Response({
                    'email/phone': email_or_phone,
                    'token': token,
                    'level': user.level
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.level
        if user_profile == 'Manager' or user_profile == 'Project-leader':
            profiles = Profile.objects.filter(user__level='Software-developer')
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

