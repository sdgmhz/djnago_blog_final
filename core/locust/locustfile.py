from locust import HttpUser, task


class QuickstartUser(HttpUser):
    """Simulates a user that logs in and makes API requests."""

    def on_start(self):
        """Authenticates the user and sets the JWT token."""
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            data={"email": "admin@admin.com", "password": "123"},
        ).json()
        self.client.headers = {
            "Authorization": f"Bearer {response.get('access', None)}"
        }

    @task
    def post_list(self):
        """Requests the list of blog posts."""
        self.client.get("/blog/api/v1/post/")

    @task
    def category_list(self):
        """Requests the list of blog categories."""
        self.client.get("/blog/api/v1/category/")
