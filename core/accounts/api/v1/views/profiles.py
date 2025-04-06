from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ..serializers import ProfileSerializer
from ....models import Profile


class ProfileApiView(RetrieveUpdateAPIView):
    """API view for retrieving and updating user profile with captcha support."""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        """Retrieve the profile object of the authenticated user."""
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
    
    def get(self, request, *args, **kwargs):
        """Retrieve user profile along with a new captcha image."""
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        new_captcha = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_captcha)
        response_data = serializer.data
        response_data.update({
            "captcha_key": new_captcha,
            "captcha_image_url": captcha_url,
        })
        return Response(response_data)
    
    def get_serializer_context(self):
        """Provide additional context for the serializer, including the authenticated user."""
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context
