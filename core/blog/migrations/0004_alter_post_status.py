# Generated by Django 4.2.19 on 2025-03-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_remove_post_category_post_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[("drf", "Draft"), ("pub", "Published")],
                default="drf",
                max_length=3,
            ),
        ),
    ]
