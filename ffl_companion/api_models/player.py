import os

import pandas as pd
from django.conf import settings
from django.db import models

from ffl_companion.api_models.owner import TeamOwner


class NFLPlayerModelManager(models.Manager):
    KEY_MAP = {
        "Name": "name",
        "Pos": "position",
        "Team": "team",
        "STD PTS": "standard_projection",
        "1/2PPR PTS": "half_ppr_projection",
        "PPR PTS": "ppr_projection",
        "Cmp": "pass_completions",
        "Att": "pass_attempts",
        "Pass Yds": "pass_yards",
        "Pass TD": "pass_td",
        "Int": "interceptions",
        "Rush": "rush_attempts",
        "Rush Yds": "rush_yards",
        "Run TD": "rush_td",
        "Tgt": "targets",
        "Rec": "receptions",
        "Rec Yds": "receiving_yards",
        "Rec TD": "receiving_td",
    }

    @classmethod
    def reset_availability(cls, player_ids: list = None):
        filters = {"id__in": player_ids} if player_ids else {}
        cls.filter(**filters).update(is_available=True)

    def import_csv_data(self, path: str):
        player_data = pd.read_csv(os.path.join(settings.BASE_DIR, path)).to_dict("records")

        to_import = []
        for player in player_data:
            player_import = {self.KEY_MAP[k]: v for k, v in player.items() if k in self.KEY_MAP}
            to_import.append(self.model(**player_import))

        self.bulk_create(to_import, ignore_conflicts=True)
        print(f"Successfully imported {len(to_import)} players")


class NFLPlayer(models.Model):
    class Meta:
        db_table = "nfl_players"
        unique_together = (("name", "position", "team", "season_start_year", "stat_type"),)

    class StatTypeChoices(models.TextChoices):
        PROJECTION = "projection"
        LIVE = "live"

    class PositionChoices(models.TextChoices):
        QB = "QB"
        WR = "WR"
        TE = "TE"
        DEF = "DEF"
        K = "K"

    name = models.CharField(max_length=255, null=False, blank=False)
    position = models.CharField(max_length=3, null=True, blank=True, choices=PositionChoices.choices)
    team = models.CharField(max_length=3, default="FA")
    standard_projection = models.FloatField(default=0.0)
    half_ppr_projection = models.FloatField(default=0.0)
    ppr_projection = models.FloatField(default=0.0)
    pass_completions = models.IntegerField(default=0)
    pass_attempts = models.IntegerField(default=0)
    pass_yards = models.IntegerField(default=0)
    pass_td = models.FloatField(default=0.0)
    interceptions = models.FloatField(default=0.0)
    rush_attempts = models.IntegerField(default=0)
    rush_yards = models.IntegerField(default=0)
    rush_td = models.FloatField(default=0.0)
    targets = models.IntegerField(default=0)
    receptions = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    receiving_td = models.FloatField(default=0.0)

    stat_type = models.CharField(max_length=255, choices=StatTypeChoices.choices, default=StatTypeChoices.PROJECTION)
    season_start_year = models.IntegerField(default=2024)

    # draft tracking
    is_available = models.BooleanField(default=True)
    fantasy_team = models.ForeignKey(TeamOwner, null=True, on_delete=models.SET_NULL, default=None, related_name="roster")

    objects = NFLPlayerModelManager()

    def save(self, *args, **kwargs):
        if self.fantasy_team and self.is_available:
            self.is_available = False

        super().save(*args, **kwargs)
