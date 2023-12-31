# Generated by Django 4.2.7 on 2023-12-13 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0005_twit_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='github_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='homepage_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
