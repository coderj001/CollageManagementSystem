# Generated by Django 4.0.5 on 2022-06-16 13:48

import django.db.models.deletion
from django.db import migrations, models

import core.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_comment_workingdays_timeslots_slotsubject_reply_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Standard",
            fields=[
                (
                    "sessionyearmodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.sessionyearmodel",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, null=True)),
                ("description", models.TextField(blank=True, max_length=500)),
            ],
            bases=("core.sessionyearmodel",),
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "subjects_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.subjects",
                    ),
                ),
                ("subject_id", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to=core.models.save_subject_image,
                        verbose_name="Subject Image",
                    ),
                ),
                ("description", models.TextField(blank=True, max_length=500)),
                (
                    "standard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subjects",
                        to="core.standard",
                    ),
                ),
            ],
            bases=("core.subjects",),
        ),
    ]