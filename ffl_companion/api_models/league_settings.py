from django.db import models

from ffl_companion.api_models.base import BaseModelManager, BaseModel


class LeagueSettingsManager(BaseModelManager):
    pass


class LeagueSettings(BaseModel):
    class Meta:
        db_table = "league_settings"
        unique_together = (("name", "setting_year"),)

    name = models.CharField(max_length=255, null=False)
    setting_year = models.IntegerField(null=False)
    playoff_teams = models.IntegerField(default=6)
    entry_price = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)
    league_host = models.CharField(max_length=255, null=True)
    league_host_url = models.CharField(max_length=255, null=True)
    league_id = models.CharField(max_length=255, null=True)

    objects = LeagueSettingsManager()

    def __str__(self):
        return self.name

    @property
    def prize_pool(self):
        return self.entry_price * self.member_count

    def save(self, *args, **kwargs):
        if not self.member_count and self.pk:
            self.member_count = self.league_stats.count()

        super().save(*args, **kwargs)


class LeagueScoringManager(BaseModelManager):
    pass


class LeagueScoring(BaseModel):
    class Meta:
        db_table = "league_scoring"
        unique_together = (("scoring_type", "stat_name"),)

    class ScoringTypeChoices(models.TextChoices):
        PASSING = "passing"
        RUSHING = "rushing"
        RECEIVING = "receiving"
        DEF = "defense"
        MISC = "misc"
        KICKING = "kicking"

    PASSING = [
        "pass_yds",
        "pass_td",
        "interceptions",
        # "two_pt_conversions",
    ]
    RECEIVING = [
        "receiving_yards",
        "receiving_td",
        "receptions",
        # "two_pt_receptions",
    ]
    RUSHING = [
        "rush_yds",
        "rush_td",
        # "two_pt_rush",
    ]

    ALL_FIELDS = [*PASSING, *RECEIVING, *RUSHING]

    scoring_type = models.CharField(max_length=50, choices=ScoringTypeChoices.choices)
    stat_name = models.CharField(max_length=50)
    point_value = models.FloatField(default=0.0)
    league_settings = models.ForeignKey(LeagueSettings, on_delete=models.SET_NULL, null=True, related_name="scoring")

    objects = LeagueScoringManager()