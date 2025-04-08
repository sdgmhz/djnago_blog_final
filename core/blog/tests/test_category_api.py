import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from blog.models import Category

User = get_user_model()


@pytest.fixture
def verified_user():
    """Fixture for creating a verified user."""
    user = User.objects.create_user(
        email="admin@admin.com", password="ax/1234567", is_verified=True
    )
    return user


@pytest.fixture
def unverified_user():
    """Fixture for creating an unverified user."""
    user = User.objects.create_user(
        email="admin@admin.com", password="ax/1234567", is_verified=False
    )
    return user


@pytest.fixture
def sample_category():
    """Fixture for creating a sample category."""
    category = Category.objects.create(name="test category")
    return category


@pytest.mark.django_db
class TestCategoryApi:
    """Test cases for category API."""

    client = APIClient()

    def test_get_category_response_200_status_guest_user(self):
        """Should return 200 for guest user when getting category list."""
        url = reverse("blog:api-v1:category-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_category_response_401_status_guest_user(self):
        """Should return 401 for guest user when creating a category."""
        url = reverse("blog:api-v1:category-list")
        data = {"name": "test_cat"}
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_category_response_403_status_unverified_user(self, unverified_user):
        """Should return 403 for unverified user when creating a category."""
        url = reverse("blog:api-v1:category-list")
        data = {"name": "test_cat"}
        self.client.force_authenticate(user=unverified_user)
        response = self.client.post(url, data)
        assert response.status_code == 403

    def test_get_category_detail_response_200_status_guest_user(self, sample_category):
        """Should return 200 for guest user when retrieving category detail."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_category_detail_response_200_status_unverified_user(
        self, sample_category, unverified_user
    ):
        """Should return 200 for unverified user when retrieving category detail."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=unverified_user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_category_detail_response_200_status_verified_user(
        self, sample_category, verified_user
    ):
        """Should return 200 for verified user when retrieving category detail."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=verified_user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_put_category_detail_response_401_status_guest_user(self, sample_category):
        """Should return 401 for guest user when updating category with PUT."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=None)
        data = {"name": "test_cat2"}
        response = self.client.put(url, data)
        assert response.status_code == 401

    def test_put_category_detail_response_403_status_unverified_user(
        self, sample_category, unverified_user
    ):
        """Should return 403 for unverified user when updating category with PUT."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=unverified_user)
        data = {"name": "test_cat2"}
        response = self.client.put(url, data)
        assert response.status_code == 403

    def test_put_category_detail_response_200_status_verified_user(
        self, sample_category, verified_user
    ):
        """Should return 200 for verified user when updating category with PUT."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=verified_user)
        data = {"name": "test_cat2"}
        response = self.client.put(url, data)
        assert response.status_code == 200

    def test_patch_category_detail_response_401_status_guest_user(
        self, sample_category
    ):
        """Should return 401 for guest user when partially updating category."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=None)
        data = {"name": "test_cat2"}
        response = self.client.patch(url, data)
        assert response.status_code == 401

    def test_patch_category_detail_response_403_status_unverified_user(
        self, sample_category, unverified_user
    ):
        """Should return 403 for unverified user when partially updating category."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=unverified_user)
        data = {"name": "test_cat2"}
        response = self.client.patch(url, data)
        assert response.status_code == 403

    def test_patch_category_detail_response_200_status_verified_user(
        self, sample_category, verified_user
    ):
        """Should return 200 for verified user when partially updating category."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=verified_user)
        data = {"name": "test_cat2"}
        response = self.client.patch(url, data)
        assert response.status_code == 200

    def test_delete_category_detail_response_401_status_guest_user(
        self, sample_category
    ):
        """Should return 401 for guest user when deleting a category."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        assert response.status_code == 401

    def test_delete_category_detail_response_403_status_unverified_user(
        self, sample_category, unverified_user
    ):
        """Should return 403 for unverified user when deleting a category."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=unverified_user)
        response = self.client.delete(url)
        assert response.status_code == 403

    def test_delete_category_detail_response_204_status_verified_user(
        self, sample_category, verified_user
    ):
        """Should return 204 for verified user when deleting a category."""
        url = reverse("blog:api-v1:category-detail", kwargs={"pk": sample_category.id})
        self.client.force_authenticate(user=verified_user)
        response = self.client.delete(url)
        assert response.status_code == 204
