# Generated by Django 4.0.5 on 2022-06-16 13:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("comm_name", models.CharField(blank=True, max_length=100)),
                ("body", models.TextField(max_length=500)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_added"],
            },
        ),
        migrations.CreateModel(
            name="WorkingDays",
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
                ("day", models.CharField(max_length=100)),
                (
                    "standard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="standard_days",
                        to="core.sessionyearmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TimeSlots",
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
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "standard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="standard_time_slots",
                        to="core.sessionyearmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SlotSubject",
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
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="standard_slots_days",
                        to="core.workingdays",
                    ),
                ),
                (
                    "slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="standard_slots_time",
                        to="core.timeslots",
                    ),
                ),
                (
                    "slot_subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="standard_slots_subject",
                        to="core.subjects",
                    ),
                ),
                (
                    "standard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="standard_slots",
                        to="core.sessionyearmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reply",
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
                ("reply_body", models.TextField(max_length=500)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "comment_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="core.comment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
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
                ("lesson_id", models.CharField(max_length=100, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=250)),
                (
                    "position",
                    models.PositiveSmallIntegerField(verbose_name="Chapter no."),
                ),
                ("slug", models.SlugField(blank=True, null=True)),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=core.models.save_lesson_files,
                        verbose_name="Video",
                    ),
                ),
                (
                    "ppt",
                    models.FileField(
                        blank=True,
                        upload_to=core.models.save_lesson_files,
                        verbose_name="Presentations",
                    ),
                ),
                (
                    "Notes",
                    models.FileField(
                        blank=True,
                        upload_to=core.models.save_lesson_files,
                        verbose_name="Notes",
                    ),
                ),
                (
                    "Standard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.sessionyearmodel",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="core.subjects",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
            },
        ),
        migrations.AddField(
            model_name="comment",
            name="lesson_name",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="core.lesson",
            ),
        ),
    ]
