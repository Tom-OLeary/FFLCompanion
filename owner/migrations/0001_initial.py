# Generated by Django 4.2.14 on 2024-08-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('dataset', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('entry_year', models.IntegerField(blank=True, null=True)),
                ('final_year', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('image', models.CharField(blank=True, max_length=50, null=True)),
                ('league_name', models.CharField(max_length=50)),
                ('password', models.CharField(default='password', max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'team_owners',
                'unique_together': {('league_name', 'name')},
            },
        ),
    ]
