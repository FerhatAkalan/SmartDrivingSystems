# Generated by Django 4.1 on 2024-05-02 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Driver",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("driver_name", models.CharField(max_length=100)),
                ("driver_surname", models.CharField(max_length=100)),
                ("driver_licence", models.CharField(max_length=50)),
                (
                    "driver_photo",
                    models.FileField(blank=True, null=True, upload_to="driver_photos/"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Trips",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField(blank=True, null=True)),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                ("car_inside_file_path", models.TextField(blank=True, null=True)),
                ("car_outside_file_path", models.TextField(blank=True, null=True)),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="report.driver"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reports",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("report_text", models.TextField()),
                ("car_inside_report_path", models.TextField()),
                ("car_outside_report_path", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("total_frames_inside", models.IntegerField()),
                ("total_frames_outside", models.IntegerField()),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="report.driver"
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="report.trips"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReportDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=10)),
                ("confidence", models.FloatField()),
                ("top_left_x", models.FloatField()),
                ("top_left_y", models.FloatField()),
                ("bottom_right_x", models.FloatField()),
                ("bottom_right_y", models.FloatField()),
                ("center_x", models.FloatField()),
                ("center_y", models.FloatField()),
                ("width", models.FloatField()),
                ("height", models.FloatField()),
                ("frame_info", models.IntegerField()),
                ("is_car_interior", models.BooleanField(default=False)),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="report.reports"
                    ),
                ),
            ],
        ),
    ]
