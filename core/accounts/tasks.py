from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import CustomUser


@shared_task
def delete_unverified_accounts_after_a_week():
    """Delete unverified user accounts that were created more than 7 days ago."""
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    unverified_users_after_a_week = CustomUser.objects.filter(
        is_verified=False, created_date__lte=seven_days_ago
    )
    unverified_users_after_a_week.delete()
