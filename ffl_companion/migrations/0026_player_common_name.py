# Generated by Django 4.2.14 on 2024-08-22 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ffl_companion', '0025_notification_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='common_name',
            field=models.CharField(blank=True, help_text='Helps to avoid duplicate names which may differ slightly between imported data sources', max_length=255, null=True),
        ),
    ]
