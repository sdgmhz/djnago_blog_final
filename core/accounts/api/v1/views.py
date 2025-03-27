from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from .serializers import RegistrationSerializer

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
        
