# Generated by Django 4.2.13 on 2024-05-29 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_courses_course_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='number_of_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]