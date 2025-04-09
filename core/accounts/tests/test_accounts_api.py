import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from captcha.models import CaptchaStore


from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture to return an instance of APIClient for making API requests."""
    return APIClient()


@pytest.fixture
def valid_registration_data():
    """Fixture to return valid data required for user registration."""
    captcha_key = CaptchaStore.generate_key()
    captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
    return {
        "email": "test10@test.com",
        "password": "ax/1234567",
        "password1": "ax/1234567",
        "captcha": captcha_obj.response,
    }


@pytest.fixture
def common_user():
    """Fixture to create and return a verified user instance."""
    user = User.objects.create_user(
        email="common_user@commonuser.com", password="ax/1234567", is_verified=True
    )
    return user


@pytest.fixture
def common_user_not_verified():
    """Fixture to create and return a non-verified user instance."""
    user = User.objects.create_user(
        email="common_user_not_verified@commonuser.com",
        password="ax/1234567",
    )
    return user


@pytest.fixture
def get_tokens_for_user(common_user):
    """Fixture to generate and return an access token for a verified user."""
    refresh = RefreshToken.for_user(common_user)
    return str(refresh.access_token)


@pytest.fixture
def get_tokens_for_not_verified_user(common_user_not_verified):
    """Fixture to generate and return an access token for a non-verified user."""
    refresh = RefreshToken.for_user(common_user_not_verified)
    return str(refresh.access_token)


@pytest.mark.django_db
class TestAccountsApi:
    """Test class to validate all user account-related API functionalities."""

    def test_user_registration_with_valid_data_201_status(
        self, api_client, valid_registration_data
    ):
        """Should return 201 and contain user email on successful registration"""
        url = reverse("accounts:api-v1:registration")
        api_client.force_authenticate(user=None)
        response = api_client.post(url, valid_registration_data)
        assert response.status_code == 201
        assert "email" in response.data

    def test_user_registration_with_invalid_data_400_status(self, api_client):
        """Should return 400 for invalid registration data"""
        url = reverse("accounts:api-v1:registration")
        invalid_data = {"email": "invalid_email", "password": "short"}
        response = api_client.post(url, invalid_data)
        assert response.status_code == 400

    def test_change_password_with_valid_data_200_status(self, api_client, common_user):
        """Should return 200 on successful password change"""
        url = reverse("accounts:api-v1:change-password")
        captcha_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
        data = {
            "old_password": "ax/1234567",
            "new_password": "com/newpass1234567",
            "new_password1": "com/newpass1234567",
            "captcha": captcha_obj.response,
        }
        api_client.force_login(user=common_user)
        response = api_client.put(url, data)
        assert response.status_code == 200
        assert "password changed successfully" in response.data["detail"]

    def test_change_password_with_invalid_data_400_status(
        self, api_client, common_user
    ):
        """Should return 400 when old password is incorrect"""
        url = reverse("accounts:api-v1:change-password")
        captcha_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
        data = {
            "old_password": "wrong_oldpass",
            "new_password": "com/newpass1234567",
            "new_password1": "com/newpass1234567",
            "captcha": captcha_obj.response,
        }
        api_client.force_login(user=common_user)
        response = api_client.put(url, data)
        assert response.status_code == 400
        assert "old password is wrong" in response.data["detail"]

    def test_token_login_with_valid_data_200_status(self, api_client, common_user):
        """Should return 200 and contain token for valid credentials"""
        url = reverse("accounts:api-v1:token-login")
        data = {"email": common_user.email, "password": "ax/1234567"}
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert "token" in response.data

    def test_token_login_with_invalid_data_400_status(self, api_client, common_user):
        """Should return 400 for invalid login credentials"""
        url = reverse("accounts:api-v1:token-login")
        data = {"email": common_user.email, "password": "axs/1234567"}
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert "token" not in response.data

    def test_token_logout_discard_token_204_status(self, api_client, common_user):
        """Should return 204 when a valid token is discarded"""
        # first obtain token for the user
        url_login = reverse("accounts:api-v1:token-login")
        data = {"email": common_user.email, "password": "ax/1234567"}
        response = api_client.post(url_login, data)
        # now check discarding the token
        url = reverse("accounts:api-v1:token-logout")
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url)
        assert response.status_code == 204

    def test_token_logout_discard_token_401_status(self, api_client, common_user):
        """Should return 401 when token logout is attempted without authentication"""
        # first obtain token for the user
        url_login = reverse("accounts:api-v1:token-login")
        data = {"email": common_user.email, "password": "ax/1234567"}
        response = api_client.post(url_login, data)
        # now check discarding the token
        url = reverse("accounts:api-v1:token-logout")
        response = api_client.post(url)
        assert response.status_code == 401

    def test_user_activation_with_valid_data_200_status(
        self, api_client, get_tokens_for_not_verified_user
    ):
        """Should return 200 when user is successfully activated with valid token"""
        token = get_tokens_for_not_verified_user
        url = reverse("accounts:api-v1:activation", kwargs={"token": token})
        response = api_client.get(url)
        assert response.status_code == 200
        assert (
            "our account has been verified and activated successfully"
            in response.data["detail"]
        )

    def test_user_activation_with_invalid_data_400_status(
        self, api_client, get_tokens_for_not_verified_user
    ):
        """Should return 400 for invalid activation token"""
        token = get_tokens_for_not_verified_user + "invaliddata"
        url = reverse("accounts:api-v1:activation", kwargs={"token": token})
        response = api_client.get(url)
        assert response.status_code == 400
        assert "token is not valid" in response.data["detail"]

    def test_user_resend_activation_with_valid_email_not_verified_200_status(
        self, api_client, common_user_not_verified
    ):
        """Should return 200 and resend activation email for a non-verified account"""
        url = reverse("accounts:api-v1:activation-resend")
        captcha_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
        data = {
            "email": common_user_not_verified.email,
            "captcha": captcha_obj.response,
        }
        api_client.force_authenticate(user=None)
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert "user activation email resend successfully" in response.data["detail"]

    def test_user_resend_activation_with_valid_email_verified_406_status(
        self, api_client, common_user
    ):
        """Should return 406 when trying to resend activation email for an already verified account"""
        url = reverse("accounts:api-v1:activation-resend")
        captcha_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
        data = {"email": common_user.email, "captcha": captcha_obj.response}
        response = api_client.post(url, data)
        assert response.status_code == 406
        assert "your account has already been verified" in response.data["detail"]

    def test_password_reset_with_valid_data_200_status(self, api_client, common_user):
        """Should return 200 and send password reset instructions to a verified user"""
        url = reverse("accounts:api-v1:password-reset")
        captcha_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
        data = {
            "email": common_user.email,
            "captcha": captcha_obj.response,
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert (
            "If there is an account with this email, we will send an password reset link for you. Check your inbox!"
            in response.data["detail"]
        )

    def test_password_reset_with_invalid_data_not_verified_user_400_status(
        self, api_client, common_user_not_verified
    ):
        """Should return 400 if password reset is requested for a non-verified user"""
        url = reverse("accounts:api-v1:password-reset")
        captcha_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
        data = {
            "email": common_user_not_verified.email,
            "captcha": captcha_obj.response,
        }
        response = api_client.post(url, data)
        assert response.status_code == 400
        assert (
            "Your account is not verified. First you should request for user verification. "
            in response.data["detail"]
        )
