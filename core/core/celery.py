import os
import django

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


django.setup()

from celery import Celery
from celery.schedules import crontab

from accounts.tasks import delete_unverified_accounts_after_a_week


app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Registers the periodic task that deletes unverified accounts to run every 10 minutes."""
    sender.add_periodic_task(
        crontab(minute="*/10"),
        delete_unverified_accounts_after_a_week.s(),
        name="Delete unverified user accounts that were created more than 7 days ago.",
    )
