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

from .serializers import RegistrationSerializer, CustomAuthTokenSerializer, CustomTokenObtainPairSerializer


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
