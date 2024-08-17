import pandas as pd

from django.db import models

from ffl_companion.api_models.base import BaseModelManager, BaseModel
from ffl_companion.api_models.import_handlers.validators import FantasyTeamImport
from ffl_companion.api_models.league_settings import LeagueSettings, LeagueScoring
from owner.models import Owner


class FantasyTeamStatsManager(BaseModelManager):
    IMPORT_MAPPING = {
        "RK": "rank",
        "TEAM": "team",
        "REC": "record",
        "PF": "points_for",
        "PA": "points_against",
        "PF/G": "ppg",
        "PA/G": "pag",
        "DIFF": "diff",
    }

    def import_season_standings(self, path: str, shared_data: dict, is_final_standing: bool = True):
        """
        shared_data {"season_start_year": 2022, "league_name": "Demo"}
        """
        data = pd.read_csv(path).to_dict("records")

        to_import = []
        for d in data:
            row = {self.IMPORT_MAPPING[k]: d[k] for k in d if k in self.IMPORT_MAPPING}
            team_import = self.model(
                **FantasyTeamImport(**row, is_final_standing=is_final_standing).data,
                **shared_data
            )
            to_import.append(team_import)

        self.bulk_create(to_import)


class FantasyTeamStats(BaseModel):
    class Meta:
        db_table = "fantasy_team_stats"
        unique_together = (("owner", "season_start_year"),)

    # standings sheet
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True, related_name="stats")
    team_name = models.CharField(max_length=50)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    total_points = models.FloatField(default=0.0)
    total_points_against = models.FloatField(default=0.0)
    ppg = models.FloatField(default=0.0)
    pag = models.FloatField(default=0.0)
    net_rating = models.IntegerField(default=0)
    regular_season_standing = models.IntegerField(default=0)
    final_season_standing = models.IntegerField(default=0)

    # calc on save
    made_playoffs = models.BooleanField(default=False)
    made_finals = models.BooleanField(default=False)
    won_finals = models.BooleanField(default=False)

    # transaction sheet
    acquisitions = models.IntegerField(default=0)
    drops = models.IntegerField(default=0)
    injured_reserve_count = models.IntegerField(default=0)
    moves = models.IntegerField(default=0)
    trades = models.IntegerField(default=0)

    # shared import
    season_start_year = models.IntegerField(default=2024)
    league_name = models.CharField(max_length=50)
    league = models.ForeignKey(LeagueSettings, on_delete=models.SET_NULL, null=True, blank=True, related_name="league_stats")

    is_current_season = models.BooleanField(default=False)

    objects = FantasyTeamStatsManager()

    def save(self, *args, **kwargs):
        if not self.made_playoffs:
            if self.final_season_standing <= self.league.playoff_teams:
                self.made_playoffs = True

        if not self.made_finals and self.final_season_standing <= 2:
            self.made_finals = True

        if not self.won_finals and self.final_season_standing == 1:
            self.won_finals = True

        super().save(*args, **kwargs)
