import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Profile
from blog.models import Post
from ..models import Comment

User = get_user_model()

now = timezone.now()


@pytest.fixture
def verified_user():
    """Creates a verified user"""
    user = User.objects.create_user(
        email="admin@admin.com", password="ax/1234567", is_verified=True
    )
    return user


@pytest.fixture
def verified_user_2():
    """Creates a verified user"""
    user = User.objects.create_user(
        email="admin5@admin.com", password="ax/1234567", is_verified=True
    )
    return user


@pytest.fixture
def unverified_user():
    """Creates an unverified user"""
    user = User.objects.create_user(
        email="admin2@admin.com", password="ax/1234567", is_verified=False
    )
    return user


@pytest.fixture
def common_post():
    """Creates a published post by an unverified user"""
    user = User.objects.create_user(
        email="admin4@admin.com", password="ax/1234567", is_verified=True
    )
    profile = Profile.objects.create(
        user=user, first_name="test first_name", last_name="test last_name"
    )
    post = Post.objects.create(
        author=profile,
        title="test title",
        content="test content",
        status="pub",
        published_date=now,
    )
    return post


@pytest.fixture
def sample_comment():
    """Creates a published post by a verified user"""
    user = User.objects.create_user(
        email="admin3@admin.com", password="ax/1234567", is_verified=True
    )
    profile = Profile.objects.create(
        user=user, first_name="test first_name", last_name="test last_name"
    )
    post = Post.objects.create(
        author=profile,
        title="test title",
        content="test content",
        status="pub",
        published_date=now,
    )
    comment = Comment.objects.create(
        post=post,
        email="admin@admin.com",
        subject="test subject",
        message="test message",
        recommend="yes",
        approved=True,
    )

    return comment


@pytest.mark.django_db
class TestCommentApi:
    client = APIClient()

    def test_get_comment_list_response_200_status_guest_user(self):
        """Should return 200 status code when guest user retrieves the comment list"""
        url = reverse("comment:api-v1:comment-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_comment_response_401_guest_user(self, common_post):
        """Should return 401 status code when guest user tries to create a comment"""
        url = reverse("comment:api-v1:comment-list")
        data = {
            "post": common_post.title,
            "email": "test@test.com",
            "subject": "test subject",
            "message": "test message",
            "recommend": "yes",
            "approved": True,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_comment_response_403_unverified_user(
        self, common_post, unverified_user
    ):
        """Should return 403 status code when unverified user tries to create a comment"""
        url = reverse("comment:api-v1:comment-list")
        data = {
            "post": common_post.title,
            "subject": "test subject2",
            "message": "test message",
            "recommend": "yes",
            "approved": True,
        }
        self.client.force_authenticate(user=unverified_user)
        response = self.client.post(url, data)
        assert response.status_code == 403

    def test_create_comment_response_201_verified_user(
        self, common_post, verified_user
    ):
        """Should return 201 status code when verified user successfully creates a comment"""
        url = reverse("comment:api-v1:comment-list")
        self.client.force_authenticate(user=verified_user)
        data = {
            "post": common_post.title,
            "subject": "test subject2",
            "message": "test message2",
            "recommend": "yes",
            "approved": True,
        }

        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get_comment_detail_response_200_status_guest_user(self, sample_comment):
        """Should return 200 status code when guest user retrieves comment details"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_comment_detail_response_200_status_unverified_user(
        self, sample_comment, unverified_user
    ):
        """Should return 200 status code when unverified user retrieves comment details"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=unverified_user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_comment_detail_response_200_status_verified_user(
        self, sample_comment, verified_user
    ):
        """Should return 200 status code when verified user retrieves comment details"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=verified_user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_put_comment_response_401_status_guest_user(
        self, sample_comment, common_post
    ):
        """Should return 401 status code when guest user tries to update a comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=None)
        data = {
            "post": common_post.title,
            "subject": "test subject3",
            "message": "test message3",
            "recommend": "no",
            "approved": True,
        }
        response = self.client.put(url, data)
        assert response.status_code == 401

    def test_put_comment_response_403_status_unverified_user(
        self, sample_comment, common_post, unverified_user
    ):
        """Should return 403 status code when unverified user tries to update a comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=unverified_user)
        data = {
            "post": common_post.title,
            "subject": "test subject3",
            "message": "test message3",
            "recommend": "no",
            "approved": True,
        }
        response = self.client.put(url, data)
        assert response.status_code == 403

    def test_put_comment_response_403_status_verified_user_not_owner(
        self, sample_comment, common_post, verified_user_2
    ):
        """Should return 403 status code when verified user (not the owner) tries to update a comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=verified_user_2)
        data = {
            "post": common_post.title,
            "subject": "test subject3",
            "message": "test message3",
            "recommend": "no",
            "approved": True,
        }
        response = self.client.put(url, data)
        assert response.status_code == 403

    def test_put_comment_response_200_status_verified_user_owner(
        self, sample_comment, common_post, verified_user
    ):
        """Should return 200 status code when verified comment owner successfully updates the comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=verified_user)
        data = {
            "post": common_post.title,
            "subject": "test subject3",
            "message": "test message3",
            "recommend": "no",
            "approved": True,
        }
        response = self.client.put(url, data)
        assert response.status_code == 200

    def test_delete_comment_response_401_status_guest_user(self, sample_comment):
        """Should return 401 status code when guest user tries to delete a comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        assert response.status_code == 401

    def test_delete_comment_response_403_status_unverified_user(
        self, sample_comment, unverified_user
    ):
        """Should return 403 status code when unverified user tries to delete a comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=unverified_user)
        response = self.client.delete(url)
        assert response.status_code == 403

    def test_delete_comment_response_403_status_verified_user_not_owner(
        self, sample_comment, verified_user_2
    ):
        """Should return 403 status code when verified user (not the owner) tries to delete a comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=verified_user_2)
        response = self.client.delete(url)
        assert response.status_code == 403

    def test_delete_comment_response_204_status_verified_user_owner(
        self, sample_comment, verified_user
    ):
        """Should return 204 status code when verified comment owner successfully deletes the comment"""
        url = reverse("comment:api-v1:comment-detail", kwargs={"pk": sample_comment.id})
        self.client.force_authenticate(user=verified_user)
        response = self.client.delete(url)
        assert response.status_code == 204
