# Generated by Django 4.2.11 on 2024-05-06 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_remove_studentcourse_course_grade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='course_image_detail',
            field=models.ImageField(blank=True, null=True, upload_to='media/course_images/'),
        ),
    ]
