import os
from datetime import date
from typing import Union

import pandas as pd
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models, IntegrityError
from django.db.models import QuerySet, Sum

from ffl_companion.api_models.choices import WeekdayChoices, PositionChoices
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.util import format_date_str
from owner.models import Owner


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
        # WEEKLY = "weekly"

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
    # stats_date = models.DateField(null=True, blank=True)

    # draft tracking
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL, default=None, related_name="players")

    objects = NFLPlayerModelManager()

    def save(self, *args, **kwargs):
        if self.owner and self.is_available:
            self.is_available = False

        super().save(*args, **kwargs)


class PlayerManager(models.Manager):
    def import_missing_players(self, data: list):
        for d in data:
            team_abbr, year = d.pop("team"), d.pop("year")
            nfl_team = NFLTeam.objects.get(abbreviation=team_abbr, season_year=year)
            try:
                player = self.create(**d)
            except IntegrityError:
                player = self.get(**d)

            if nfl_team not in player.nfl_teams.all():
                player.nfl_teams.add(nfl_team)


class Player(models.Model):
    SUFFIXES = [
        "Jr",
        "Sr",
        "II",
        "III",
        "IV",
        "V",
    ]

    class Meta:
        db_table = "players"
        unique_together = (("name", "position"),)

    name = models.CharField(max_length=255, null=False, blank=False)
    position = models.CharField(max_length=4, null=False, blank=False, choices=PositionChoices.choices)
    nfl_teams = models.ManyToManyField(NFLTeam, related_name="team_players")
    common_name = models.CharField(max_length=255, null=True, blank=True, help_text="Helps to avoid duplicate names which may differ slightly between imported data sources")

    objects = PlayerManager()

    @classmethod
    def stats_by_year(cls, year: int, player_ids: list) -> QuerySet:
        return cls.objects.filter(stats_weekly__season_start_year=year, player_id__in=player_ids)

    @property
    def current_team(self):
        return self.nfl_teams.order_by("-season_year").first()

    @property
    def fantasy_points(self):
        """Calculate total fantasy points for this player during given week"""
        roster = self.player_rosters.filter(roster_year=settings.CURRENT_YEAR).first()
        if roster is None:
            return 0

        total = 0
        scoring = roster.league.scoring.all()
        for stat in self.stats_weekly.filter(season_start_year=settings.CURRENT_YEAR):
            for s in scoring:
                stat_value = getattr(stat, s.stat_name)
                total += stat_value * s.point_value

        return total

    def is_available(self, dataset: str):
        return not self.player_rosters.filter(roster_year=settings.CURRENT_YEAR, dataset=dataset).exists()
    
    def weekly_stats_by_year(self, year: int) -> QuerySet:
        return self.stats_weekly.filter(season_start_year=year)

    def season_totals(self, year: int, fields: list, trade_date: Union[str, date] = None) -> QuerySet:
        sum_totals = {f: Sum(f) for f in fields}
        stats_filter = {"season_start_year": year}
        if trade_date:
            stats_filter["game_date__gte"] = trade_date

        return self.stats_weekly.filter(**stats_filter).values("player_id").annotate(**sum_totals)

    def set_common_name(self):
        common_name = self.name.replace(".", "")
        for suffix in self.SUFFIXES:
            if suffix in common_name:
                common_name = common_name.replace(suffix, "")

        self.common_name = common_name.lower().replace(" ", "")

    def save(self, *args, **kwargs):
        if not self.common_name:
            self.set_common_name()

        super().save(*args, **kwargs)


class PlayerStatsManager(models.Manager):
    MAPPINGS = {
        "passing": {
            "Player": "player_name",
            "Rate": "pass_rating",
            "Att": "pass_attempts",
            "Day": "day_of_week",
            "Week": "game_week",
            "Date": "game_date",
            "Team": "team",
            "Opp": "opponent",
            "Cmp": "pass_completions",
            "Cmp%": "pass_completion_pct",
            "Yds": "pass_yds",
            "TD": "pass_td",
            "Int": "interceptions",
            "Pos.": "position",
        },
        "receiving": {
            "Player": "player_name",
            "Yds": "receiving_yards",
            "Tgt": "targets",
            "Day": "day_of_week",
            "Week": "game_week",
            "Date": "game_date",
            "Team": "team",
            "Opp": "opponent",
            "Rec": "receptions",
            "TD": "receiving_td",
            "Pos.": "position"
        },
        "rushing": {
            "Player": "player_name",
            "Yds": "rush_yds",
            "Att": "rush_attempts",
            "Day": "day_of_week",
            "Week": "game_week",
            "Date": "game_date",
            "Team": "team",
            "Opp": "opponent",
            "TD": "rush_td",
            "Pos.": "position"
        },
    }

    TEAM_MAPPING = {
        "NYG": "NYG",
        "PHI": "PHI",
        "HOU": "HOU",
        "CHI": "CHI",
        "CIN": "CIN",
        "SEA": "SEA",
        "SFO": "SF",
        "IND": "IND",
        "LAR": "LAR",
        "TAM": "TB",
        "CAR": "CAR",
        "ATL": "ATL",
        "DET": "DET",
        "MIA": "MIA",
        "PIT": "PIT",
        "DAL": "DAL",
        "DEN": "DEN",
        "NOR": "NO",
        "LVR": "LV",
        "BUF": "BUF",
        "KAN": "KC",
        "BAL": "BAL",
        "NWE": "NE",
        "GNB": "GB",
        "WAS": "WAS",
        "CLE": "CLE",
        "ARI": "ARI",
        "MIN": "MIN",
        "LAC": "LAC",
        "TEN": "TEN",
        "JAX": "JAX",
        "NYJ": "NYJ"
    }

    def import_csv_data(self, path: str, stat_type: str, year: int):
        key_mapping = self.MAPPINGS[stat_type]

        data = pd.read_csv(path).to_dict("records")
        for d in data:
            row = {key_mapping[k]: d[k] for k in key_mapping}
            team_abbr = row.pop("team")
            if isinstance(team_abbr, float):
                continue
            team = self.TEAM_MAPPING[team_abbr]
            try:
                NFLTeam.objects.get(abbreviation=team, season_year=year)
            except NFLTeam.DoesNotExist:
                print("STATS IMPORT TEAM NOT FOUND", year, team)
                continue

            player_name = row.pop("player_name")
            position = row.pop("position")
            try:
                player = Player.objects.get(name=player_name, position=position)
            except Player.DoesNotExist:
                print("STATS IMPORT Player not found", player_name, position)
                continue

            row["player"] = player
            row["game_date"] = format_date_str(row["game_date"])
            row["season_start_year"] = year

            try:
                self.get(player=player, season_start_year=year, game_week=row["game_week"])
            except PlayerStatsWeekly.DoesNotExist:
                self.create(**row)
            else:
                self.filter(player=player, season_start_year=year, game_week=row["game_week"]).update(**row)

    def find_missing(self, data: list, stat_type: str, year: int):
        key_mapping = self.MAPPINGS[stat_type]

        players_not_found = []
        for d in data:
            row = {key_mapping[k]: d[k] for k in key_mapping}
            team_abbr = row.pop("team")
            if isinstance(team_abbr, float):
                continue

            team = self.TEAM_MAPPING[team_abbr]
            player_name = row.pop("player_name")
            position = row.pop("position")
            try:
                Player.objects.get(name=player_name, position=position)
            except Player.DoesNotExist:
                print("Player not found", player_name, position)
                players_not_found.append({"name": player_name, "position": position, "team": team, "year": year})

        return players_not_found


class PlayerStatsWeekly(models.Model):
    class Meta:
        db_table = "player_stats_weekly"
        unique_together = (("player_id", "season_start_year", "game_week"),)

    PASSING = [
        "pass_yds",
        "pass_td",
        "pass_attempts",
        "pass_completions",
        "interceptions",
    ]
    RECEIVING = [
        "targets",
        "receptions",
        "receiving_yards",
        "receiving_td",
    ]
    RUSHING = [
        "rush_yds",
        "rush_td",
        "rush_attempts",
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="stats_weekly")
    season_start_year = models.IntegerField(default=2024, db_index=True)
    day_of_week = models.CharField(max_length=9, choices=WeekdayChoices.choices, default=WeekdayChoices.SUN)
    game_date = models.DateField(null=False, blank=False)
    game_week = models.IntegerField(null=False, blank=False, validators=[MaxValueValidator(18)])
    opponent = models.CharField(max_length=3, null=False, blank=False)

    # passing
    pass_yds = models.IntegerField(default=0)
    pass_td = models.IntegerField(default=0)
    pass_attempts = models.IntegerField(default=0)
    pass_completions = models.IntegerField(default=0)
    interceptions = models.IntegerField(default=0)
    pass_completion_pct = models.FloatField(default=0.0)
    pass_rating = models.FloatField(default=0.0)

    # rushing
    rush_yds = models.IntegerField(default=0)
    rush_td = models.IntegerField(default=0)
    rush_attempts = models.IntegerField(default=0)

    # receiving
    targets = models.IntegerField(default=0)
    receptions = models.IntegerField(default=0)
    receiving_yards = models.IntegerField(default=0)
    receiving_td = models.IntegerField(default=0)

    objects = PlayerStatsManager()

    @property
    def fantasy_points(self):
        """Calculate total fantasy points for this player during given week"""
        roster = self.player.player_rosters.filter(roster_year=self.season_start_year).first()
        if roster is None:
            return 0

        total = 0
        scoring = roster.league.scoring.all()
        for s in scoring:
            stat_value = getattr(self, s.stat_name)
            total += stat_value * s.point_value

        return total
