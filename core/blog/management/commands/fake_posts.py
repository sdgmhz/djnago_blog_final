from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone

from accounts.models import CustomUser, Profile
from blog.models import Post, Category

# Get the current timestamp to use for post publishing
now = timezone.now()


class Command(BaseCommand):
    """Management command for inserting dummy data"""

    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        """Initialize the command and setup Faker"""
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        """Generate fake user, profile, and blog posts"""

        # Create a new fake user
        user = CustomUser.objects.create_user(
            email=self.fake.email(), password="ax/1234567", is_verified=True
        )
        # Access and fill the user's profile
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=2)
        profile.save()
        # Create 10 dummy blog posts with random categories
        for _ in range(10):
            post = Post.objects.create(
                author=profile,
                title=" ".join(self.fake.words(3)),
                content=self.fake.paragraph(nb_sentences=5),
                status="pub",
                published_date=now,
            )
            # Assign 1 to 3 random categories to the post
            post.category.set(
                random.sample(list(Category.objects.all()), k=random.randint(1, 3))
            )
