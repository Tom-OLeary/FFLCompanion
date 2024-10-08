# Generated by Django 4.2.14 on 2024-07-28 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ffl_companion', '0015_teamowner_last_login_teamowner_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='fantasyteamstats',
            name='dataset',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='leaguesettings',
            name='dataset',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='dataset',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='roster',
            name='dataset',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='teamowner',
            name='dataset',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='trade',
            name='dataset',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
