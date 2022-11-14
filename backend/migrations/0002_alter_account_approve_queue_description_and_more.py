# Generated by Django 4.1.1 on 2022-11-10 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account_approve_queue",
            name="Description",
            field=models.TextField(verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="account_approve_queue",
            name="Permission",
            field=models.IntegerField(verbose_name="Permission"),
        ),
        migrations.AlterField(
            model_name="user_profile",
            name="Gender",
            field=models.IntegerField(
                choices=[(0, "male"), (1, "female")], verbose_name="Gender"
            ),
        ),
    ]
