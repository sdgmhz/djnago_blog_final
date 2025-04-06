# Generated by Django 4.2.20 on 2025-04-03 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedPasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['token'], name='accounts_us_token_887108_idx'), models.Index(fields=['user'], name='accounts_us_user_id_f8d9ab_idx')],
            },
        ),
    ]
