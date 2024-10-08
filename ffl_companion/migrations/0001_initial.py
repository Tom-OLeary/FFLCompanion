# Generated by Django 4.2.14 on 2024-07-24 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeamOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('entry_year', models.IntegerField(blank=True, null=True)),
                ('final_year', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('image', models.FilePathField(blank=True, null=True, path='/img')),
                ('league_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'owners',
                'unique_together': {('league_name', 'name')},
            },
        ),
        migrations.CreateModel(
            name='LeagueSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('setting_year', models.IntegerField()),
                ('playoff_teams', models.IntegerField(default=6)),
                ('entry_price', models.IntegerField(default=0)),
                ('member_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'league_settings',
                'unique_together': {('name', 'setting_year')},
            },
        ),
        migrations.CreateModel(
            name='NFLPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(blank=True, choices=[('QB', 'Qb'), ('WR', 'Wr'), ('TE', 'Te'), ('DEF', 'Def'), ('K', 'K')], max_length=3, null=True)),
                ('team', models.CharField(default='FA', max_length=3)),
                ('standard_projection', models.FloatField(default=0.0)),
                ('half_ppr_projection', models.FloatField(default=0.0)),
                ('ppr_projection', models.FloatField(default=0.0)),
                ('pass_completions', models.IntegerField(default=0)),
                ('pass_attempts', models.IntegerField(default=0)),
                ('pass_yards', models.IntegerField(default=0)),
                ('pass_td', models.FloatField(default=0.0)),
                ('interceptions', models.FloatField(default=0.0)),
                ('rush_attempts', models.IntegerField(default=0)),
                ('rush_yards', models.IntegerField(default=0)),
                ('rush_td', models.FloatField(default=0.0)),
                ('targets', models.IntegerField(default=0)),
                ('receptions', models.IntegerField(default=0)),
                ('receiving_yards', models.IntegerField(default=0)),
                ('receiving_td', models.FloatField(default=0.0)),
                ('stat_type', models.CharField(choices=[('projection', 'Projection'), ('live', 'Live')], default='projection', max_length=255)),
                ('season_start_year', models.IntegerField(default=2024)),
                ('is_available', models.BooleanField(default=True)),
                ('fantasy_team', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='roster', to='ffl_companion.teamowner')),
            ],
            options={
                'db_table': 'nfl_players',
                'unique_together': {('name', 'position', 'team', 'season_start_year', 'stat_type')},
            },
        ),
        migrations.CreateModel(
            name='FantasyTeamStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=50)),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('draws', models.IntegerField(default=0)),
                ('total_points', models.FloatField(default=0.0)),
                ('total_points_against', models.FloatField(default=0.0)),
                ('ppg', models.FloatField(default=0.0)),
                ('pag', models.FloatField(default=0.0)),
                ('net_rating', models.IntegerField(default=0)),
                ('regular_season_standing', models.IntegerField(default=0)),
                ('final_season_standing', models.IntegerField(default=0)),
                ('made_playoffs', models.BooleanField(default=False)),
                ('made_finals', models.BooleanField(default=False)),
                ('won_finals', models.BooleanField(default=False)),
                ('acquisitions', models.IntegerField(default=0)),
                ('drops', models.IntegerField(default=0)),
                ('injured_reserve_count', models.IntegerField(default=0)),
                ('moves', models.IntegerField(default=0)),
                ('trades', models.IntegerField(default=0)),
                ('season_start_year', models.IntegerField(default=2024)),
                ('league_name', models.CharField(max_length=50)),
                ('league', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='league_stats', to='ffl_companion.leaguesettings')),
                ('team_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_stats', to='ffl_companion.teamowner')),
            ],
            options={
                'db_table': 'fantasy_team_stats',
                'unique_together': {('team_owner', 'season_start_year')},
            },
        ),
    ]
