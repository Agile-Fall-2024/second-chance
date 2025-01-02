# Generated by Django 5.1.4 on 2025-01-01 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("advertisement", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="advertisement",
            name="category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="advertisements",
                to="advertisement.category",
            ),
            preserve_default=False,
        ),
    ]
