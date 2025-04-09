import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Profile
from blog.models import Post

User = get_user_model()


@pytest.fixture
def verified_user():
    """Creates a verified user"""
    user = User.objects.create_user(
        email="admin@admin.com", password="ax/1234567", is_verified=True
    )
    return user


@pytest.fixture
def unverified_user():
    """Creates an unverified user"""
    user = User.objects.create_user(
        email="admin@admin.com", password="ax/1234567", is_verified=False
    )
    return user


@pytest.fixture
def common_post_by_verified_user():
    """Creates a published post by a verified user"""
    user = User.objects.create_user(
        email="admin@admin.com", password="ax/1234567", is_verified=True
    )
    profile = Profile.objects.create(
        user=user, first_name="test first_name", last_name="test last_name"
    )
    post = Post.objects.create(
        author=profile,
        title="test title",
        content="test content",
        status="pub",
        published_date=timezone.now(),
    )
    return post


@pytest.fixture
def common_post_by_unverified_user():
    """Creates a published post by an unverified user"""
    user = User.objects.create_user(
        email="admin@admin.com", password="ax/1234567", is_verified=False
    )
    profile = Profile.objects.create(
        user=user, first_name="test first_name", last_name="test last_name"
    )
    post = Post.objects.create(
        author=profile,
        title="test title",
        content="test content",
        status="pub",
        published_date=timezone.now(),
    )
    return post


@pytest.mark.django_db
class TestPostApi:
    """Tests for Post API endpoints"""

    client = APIClient()

    def test_get_posts_response_200_status_guest_user(self):
        """Should return 200 OK for guest user when listing posts"""
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_posts_response_200_status_unverified_user(self, unverified_user):
        """Should return 200 OK for unverified user when listing posts"""
        url = reverse("blog:api-v1:post-list")
        self.client.force_authenticate(user=unverified_user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_posts_response_200_status_verified_user(self, verified_user):
        """Should return 200 OK for verified user when listing posts"""
        url = reverse("blog:api-v1:post-list")
        self.client.force_authenticate(user=verified_user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status_guest_user(self):
        """Should return 401 Unauthorized when guest user tries to create a post"""
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": "pub",
            "published_date": datetime.now(),
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_post_response_403_status_unverified_user(self, unverified_user):
        """Should return 403 Forbidden when unverified user tries to create a post"""
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": "pub",
            "published_date": datetime.now(),
        }
        self.client.force_authenticate(user=unverified_user)
        response = self.client.post(url, data)
        assert response.status_code == 403

    def test_create_post_response_201_status_verified_user(self, verified_user):
        """Should return 201 Created when verified user creates a post"""
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test",
            "content": "description",
            "status": "pub",
            "published_date": datetime.now(),
        }
        self.client.force_authenticate(user=verified_user)
        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_create_post_invalid_data_response_400_status_verified(self, verified_user):
        """Should return 400 Bad Request when verified user submits invalid post data"""
        url = reverse("blog:api-v1:post-list")
        data = {"title": "test", "content": "description"}
        self.client.force_authenticate(user=verified_user)
        response = self.client.post(url, data)
        assert response.status_code == 400

    def test_get_post_detail_response_200_status_guest_user(
        self, common_post_by_verified_user
    ):
        """Should return 200 OK when guest user retrieves a post detail"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_verified_user.id}
        )
        response = self.client.get(url)
        assert response.status_code == 200

    def test_put_post_detail_response_401_status_guest_user(
        self, common_post_by_verified_user
    ):
        """Should return 401 Unauthorized when guest user tries to update a post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_verified_user.id}
        )
        data = {
            "title": "test2",
            "content": "description2",
            "status": "pub",
            "published_date": datetime.now(),
        }
        self.client.force_authenticate(user=None)
        response = self.client.put(url, data)
        assert response.status_code == 401

    def test_put_post_detail_response_200_status_verified_user(
        self, common_post_by_verified_user
    ):
        """Should return 200 OK when verified user updates their own post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_verified_user.id}
        )
        data = {
            "title": "test2",
            "content": "description2",
            "status": "pub",
            "published_date": datetime.now(),
        }
        self.client.force_authenticate(user=common_post_by_verified_user.author.user)
        response = self.client.put(url, data)
        assert response.status_code == 200

    def test_put_post_detail_response_403_status_unverified_user(
        self, common_post_by_unverified_user
    ):
        """Should return 403 Forbidden when unverified user tries to update a post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_unverified_user.id}
        )
        data = {
            "title": "test2",
            "content": "description2",
            "status": "pub",
            "published_date": datetime.now(),
        }
        self.client.force_authenticate(user=common_post_by_unverified_user.author.user)
        response = self.client.put(url, data)
        assert response.status_code == 403

    def test_patch_post_detail_response_403_status_guest_user(
        self, common_post_by_verified_user
    ):
        """Should return 403 Forbidden when guest user tries to partially update a post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_verified_user.id}
        )
        data = {
            "title": "test2",
            "content": "description2",
        }
        response = self.client.patch(url, data)
        assert response.status_code == 403

    def test_patch_post_detail_response_200_status_verified_user(
        self, common_post_by_verified_user
    ):
        """Should return 200 OK when verified user partially updates their own post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_verified_user.id}
        )
        data = {
            "title": "test2",
            "content": "description2",
        }
        self.client.force_authenticate(user=common_post_by_verified_user.author.user)
        response = self.client.patch(url, data)
        assert response.status_code == 200

    def test_patch_post_detail_response_403_status_unverified_user(
        self, common_post_by_unverified_user
    ):
        """Should return 403 Forbidden when unverified user tries to partially update a post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_unverified_user.id}
        )
        data = {
            "title": "test2",
            "content": "description2",
        }
        self.client.force_authenticate(user=common_post_by_unverified_user.author.user)
        response = self.client.put(url, data)
        assert response.status_code == 403

    def test_delete_post_detail_response_403_status_guest_user(
        self, common_post_by_verified_user
    ):
        """Should return 403 Forbidden when guest user tries to delete a post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_verified_user.id}
        )
        response = self.client.delete(url)
        assert response.status_code == 403

    def test_delete_post_detail_response_204_status_verified_user(
        self, common_post_by_verified_user
    ):
        """Should return 204 No Content when verified user deletes their own post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_verified_user.id}
        )
        self.client.force_authenticate(user=common_post_by_verified_user.author.user)
        response = self.client.delete(url)
        assert response.status_code == 204

    def test_delete_post_detail_response_403_status_unverified_user(
        self, common_post_by_unverified_user
    ):
        """Should return 403 Forbidden when unverified user tries to delete a post"""
        url = reverse(
            "blog:api-v1:post-detail", kwargs={"pk": common_post_by_unverified_user.id}
        )
        self.client.force_authenticate(user=common_post_by_unverified_user.author.user)
        response = self.client.delete(url)
        assert response.status_code == 403

    def test_post_list_content(self, common_post_by_verified_user):
        """Checks if post list includes a known post title"""
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        response_data = response.json()
        posts = response_data.get("results")
        posts_title = [post.get("title") for post in posts]
        assert common_post_by_verified_user.title in posts_title
