# Generated by Django 4.1.1 on 2022-12-24 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0003_reply"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reply",
            old_name="AttachedNId",
            new_name="AttachedPId",
        ),
    ]
