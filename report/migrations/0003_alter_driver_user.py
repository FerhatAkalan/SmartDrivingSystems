# Generated by Django 4.1 on 2024-04-28 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("report", "0002_alter_trips_end_time_alter_trips_start_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
