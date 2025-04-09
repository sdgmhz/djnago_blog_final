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
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, DecodeError
from django.contrib.auth import logout
from django.utils import timezone
import uuid
from ..serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ActivationResendAndPasswordResetSerializer,
    PasswordResetConfirmSerializer,
)
from ...utils import EmailThread
from ....models import UsedPasswordResetToken

User = get_user_model()


class RegistrationApiView(GenericAPIView):
    """API view for user registration including captcha generation and validation."""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """Processes user registration, sends activation email, and returns response."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"email": serializer.validated_data["email"]}
            user_obj = get_object_or_404(User, email=data["email"])
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token, "email": data["email"], "request": request},
                "admin@admin.com",
                to=[data["email"]],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """Generates and returns a new captcha challenge with key and image URL."""
        new_captcha = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_captcha)

        return Response({"captcha_key": new_captcha, "captcha_image_url": captcha_url})

    def get_tokens_for_user(self, user):
        """Generates and returns JWT access token for the given user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    """API view for user authentication and token generation."""

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """Authenticate user and return an auth token."""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


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
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"detail": "old password is wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """Generate and return a new captcha for password change validation."""
        new_captcha = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_captcha)

        return Response({"captcha_key": new_captcha, "captcha_image_url": captcha_url})


class ActivationApiView(APIView):
    """API view for handling account activation via token."""

    def get(self, request, token, *args, **kwargs):
        """Handles GET request to activate user account with the given token."""
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "token has been expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except DecodeError:
            return Response(
                {"detail": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"detail": "Your account has already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"detail": "Your account has been verified and activated successfully"},
            status=status.HTTP_200_OK,
        )


class ActivationResendApiView(GenericAPIView):
    """API view for resending the activation email."""

    serializer_class = ActivationResendAndPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """Handles POST request to resend activation email."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if not user_obj.is_verified:
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token, "email": email},
                "admin@admin.com",
                to=[email],
            )

            EmailThread(email_obj).start()
            return Response(
                {"detail": "user activation email resend successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "your account has already been verified"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    def get_tokens_for_user(self, user):
        """Generates JWT access token for the given user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get(self, request, *args, **kwargs):
        """Handles GET request to generate and return a new captcha image."""
        new_captcha = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_captcha)
        return Response({"captcha_key": new_captcha, "captcha_image_url": captcha_url})


class PasswordResetApiView(GenericAPIView):
    """Handles password reset requests including email verification and captcha generation."""

    serializer_class = ActivationResendAndPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        """Processes password reset request and sends reset link if email is valid and verified."""

        # Check if user is authenticated
        if request.user.is_authenticated:
            logout(request)  # Logout the user automatically
            return Response(
                {
                    "detail": "You were automatically logged out to process your password reset request."
                },
                status=status.HTTP_200_OK,
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            # according to security considerations, we will not tell the user if there is no account associated with this email or not!!
            return Response(
                {
                    "detail": "If there is an account with this email, we will send an password reset link for you. Check your inbox!"
                },
                status=status.HTTP_200_OK,
            )
        if user_obj.is_verified:
            token = self.get_unique_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/password_reset_email.tpl",
                {"token": token, "email": email},
                "admin@admin.com",
                to=[email],
            )

            EmailThread(email_obj).start()
            # according to security considerations, we will not tell the user if there is no account associated with this email or not!!
            return Response(
                {
                    "detail": "If there is an account with this email, we will send an password reset link for you. Check your inbox!"
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "detail": "Your account is not verified. First you should request for user verification. "
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_unique_tokens_for_user(self, user):
        """Generates JWT access token for the given user."""
        payload = {
            "user_id": user.id,
            "timestamp": timezone.now().isoformat(),
            "unique_id": str(uuid.uuid4()),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # save token in db
        UsedPasswordResetToken.objects.create(user=user, token=token, used=False)
        return token

    def get(self, request, *args, **kwargs):
        """Generates and returns a new captcha challenge for password reset form."""
        # Check if user is authenticated
        if request.user.is_authenticated:
            logout(request)  # Logout the user automatically
            return Response(
                {
                    "detail": "You were automatically logged out to process your password reset request."
                },
                status=status.HTTP_200_OK,
            )
        new_captcha = CaptchaStore.generate_key()
        captcha_url = captcha_image_url(new_captcha)
        return Response({"captcha_key": new_captcha, "captcha_image_url": captcha_url})


class PasswordResetConfirmApiView(GenericAPIView):
    """Handles password reset confirmation including token validation and password update."""

    serializer_class = PasswordResetConfirmSerializer

    def get(self, request, token, *args, **kwargs):
        """Validates reset token and returns user info with new captcha challenge."""
        try:
            # decode token and find the user_id
            token_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token_data.get("user_id")
            token_obj = UsedPasswordResetToken.objects.get(token=token)
            # check if the token have been used before or not
            if token_obj.used:
                return Response(
                    {
                        "detail": "This link has been used before. Please request a new link."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            new_captcha = CaptchaStore.generate_key()
            captcha_url = captcha_image_url(new_captcha)
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except DecodeError:
            return Response(
                {"detail": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        # find user
        user_obj = User.objects.get(pk=user_id)
        return Response(
            {
                "detail": f"Password reset for user: {user_obj.email}",
                "captcha_key": new_captcha,
                "captcha_image_url": captcha_url,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, token, *args, **kwargs):
        """Processes password update after validating token and new password requirements."""
        try:
            # decode token and find the user_id
            token_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token_data.get("user_id")
            # find user for resetting password
            user_obj = User.objects.get(pk=user_id)
            token_obj = UsedPasswordResetToken.objects.get(token=token)
            if token_obj.used:
                return Response(
                    {
                        "detail": "This link has been used before. Please request a new link."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():

                # set the new password
                user_obj.set_password(serializer.data.get("new_password"))
                user_obj.save()
                # mark the token as a used token
                token_obj.used = True
                token_obj.save()

                return Response(
                    {
                        "detail": f"password reset successfully for user:{user_obj.email}"
                    },
                    status=status.HTTP_200_OK,
                )
        except ExpiredSignatureError:
            return Response(
                {"detail": "Token has been expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except DecodeError:
            return Response(
                {"detail": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
