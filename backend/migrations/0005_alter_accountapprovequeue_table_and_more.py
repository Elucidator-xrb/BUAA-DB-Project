# Generated by Django 4.1.1 on 2022-11-12 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0004_alter_useraccount_permission"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="accountapprovequeue",
            table="account_approve_queue",
        ),
        migrations.AlterModelTable(
            name="useraccount",
            table="user_account",
        ),
        migrations.AlterModelTable(
            name="userprofile",
            table="user_profile",
        ),
    ]
