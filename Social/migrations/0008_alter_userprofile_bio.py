# Generated by Django 4.2.7 on 2023-12-13 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0007_alter_userprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
