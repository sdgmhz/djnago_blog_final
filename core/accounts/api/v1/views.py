from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegistrationSerializer, CustomAuthTokenSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer


class RegistrationApiView(GenericAPIView):
    """API view for user registration with captcha validation."""
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """Handles user registration with validation and captcha verification."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'email': serializer.validated_data['email']}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """Generates and returns a new captcha image and key."""
        new_captcha = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_captcha)

        return Response({"captcha_key": new_captcha, "captcha_image_url": captcha_url})


class CustomObtainAuthToken(ObtainAuthToken):
    """API view for user authentication and token generation."""
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """Authenticate user and return an auth token."""
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomDiscardAuthToken(APIView):
    """API view for logging out by deleting the user's auth token."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Delete the auth token to log the user out."""
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """View for obtaining a JWT token pair using a custom serializer."""
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(GenericAPIView):
    """API view for changing user password with authentication and captcha support."""

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        """Retrieve the authenticated user object."""
        return self.request.user

    def put(self, request, *args, **kwargs):
        """Handle password change request after validating old password and new password."""
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"detail": "old password is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'detail': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """Generate and return a new captcha for password change validation."""
        new_captcha = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_captcha)

        return Response({"captcha_key": new_captcha, "captcha_image_url": captcha_url})
