# Generated by Django 5.0.3 on 2024-08-07 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_userprofile_user"),
        ("vendor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewratting",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
            ),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to="accounts.user",
            ),
        ),
    ]
