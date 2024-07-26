# Generated by Django 4.2.14 on 2024-07-26 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ffl_companion', '0012_trade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='owners',
        ),
        migrations.RemoveField(
            model_name='trade',
            name='players',
        ),
        migrations.AddField(
            model_name='trade',
            name='owner_one',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_one_trades', to='ffl_companion.teamowner'),
        ),
        migrations.AddField(
            model_name='trade',
            name='owner_one_received',
            field=models.ManyToManyField(related_name='owner_one_received', to='ffl_companion.player'),
        ),
        migrations.AddField(
            model_name='trade',
            name='owner_two',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_two_trades', to='ffl_companion.teamowner'),
        ),
        migrations.AddField(
            model_name='trade',
            name='owner_two_received',
            field=models.ManyToManyField(related_name='owner_two_received', to='ffl_companion.player'),
        ),
    ]
