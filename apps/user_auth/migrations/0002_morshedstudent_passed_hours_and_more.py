# Generated by Django 4.2.11 on 2024-05-05 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='morshedstudent',
            name='passed_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='morshedstudent',
            name='registered_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]