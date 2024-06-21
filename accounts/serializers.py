from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'level']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            phone=validated_data['phone'],
            level=validated_data['level'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # Deactivate account until it is verified
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            self.fail('bad_token')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'designation', 'address', 'phoneno', 'salary', 'image']

