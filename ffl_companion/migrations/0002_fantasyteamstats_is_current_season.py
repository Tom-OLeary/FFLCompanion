# Generated by Django 4.2.14 on 2024-07-25 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ffl_companion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fantasyteamstats',
            name='is_current_season',
            field=models.BooleanField(default=False),
        ),
    ]
