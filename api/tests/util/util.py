from collections import defaultdict
from datetime import date

from django.conf import settings
from django.db import IntegrityError
from rest_framework.test import APITestCase

from api.tests.util.fixtures import PLAYER_STATS
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.player import Player, PlayerStatsWeekly
from ffl_companion.api_models.roster import Roster
from owner.models import Owner


class BaseTestCase(APITestCase):
    IMPORT_DATA = None
    leagues: list[LeagueSettings] = None
    owners: list[Owner] = None
    stats: list[FantasyTeamStats] = None
    players: list[Player] = None
    rosters: list[Roster] = None
    player_stats: list[PlayerStatsWeekly] = None

    @classmethod
    def setUpTestData(cls):
        cls.user = Owner.objects.create_owner(
            name="User1",
            username="test.owner",
            password="password",
            dataset="testing",
        )

        if cls.IMPORT_DATA:
            for attr, model, fixture in cls.IMPORT_DATA:
                data = bulk_create(model, fixture)
                setattr(cls, attr, data)

    def setUp(self):
        self.client.force_authenticate(self.user)
        self.generate_data()

    def generate_data(self):
        self.link_leagues()
        self.roster = self.query_model(Roster).get(roster_year=2024)
        self.league = self.query_model(LeagueSettings).get(setting_year=2024)
        self.roster.owner = self.user
        self.roster.league = self.league
        self.roster.save()

    def link_leagues(self):
        for league in self.leagues:
            year = league.setting_year
            FantasyTeamStats.objects.filter(season_start_year=year).update(league=league)

        for year in [2019, 2020, 2021, 2022, 2023]:
            stats = FantasyTeamStats.objects.filter(season_start_year=year).order_by("team_name")
            owners = Owner.objects.order_by("name")
            for owner, stat in zip(owners, stats):
                stat.owner = owner
                stat.save()

    def link_player_stats(self):
        current_week, i = 0, 0
        player = self.players[0]
        for stat in PLAYER_STATS:
            if stat["game_week"] < current_week:
                i += 1
                try:
                    player = self.players[i]
                except IndexError:
                    continue
            current_week = stat["game_week"]
            stat["player_id"] = player.id
            PlayerStatsWeekly.objects.create(**stat)

    def generate_rosters(self):
        positions = ["QB", "RB", "WR", "TE", "DEF"]
        for i in range(1, 6):
            roster = Roster.objects.create(roster_year=settings.CURRENT_YEAR, league=self.league, dataset="testing")
            for pos in positions:
                player = Player.objects.create(name=f"{pos}{i}", position=pos)
                stats = MockStats(position=pos, initial_value=i)()
                stats["player"] = player
                PlayerStatsWeekly.objects.create(**stats)
                roster.players.add(player)

    @staticmethod
    def query_model(model):
        return model.objects.filter(dataset="testing")


def bulk_create(model, rows):
    to_create = [model(**r) for r in rows]
    return model.objects.bulk_create(to_create)


class MockStats:
    _QB = [
        "pass_yds",
        "pass_td",
        "pass_attempts",
        "pass_completions",
        "interceptions",
        "pass_completion_pct",
        "pass_rating",
    ]
    _REC = [
        "targets",
        "receptions",
        "receiving_yards",
        "receiving_td",
    ]
    _RUSH = [
        "rush_yds",
        "rush_td",
        "rush_attempts",
    ]
    _MODIFIERS = {
        100: [
            "pass_yds",
            "receiving_yards",
        ],
        10: [
            "pass_attempts",
            "pass_completions",
            "pass_completion_pct",
            "pass_rating",
            "rush_yds",
            "rush_attempts"
        ],
        1: [
            "pass_td",
            "interceptions",
            "targets",
            "receptions",
            "receiving_td",
            "rush_td",
        ],
    }
    STAT_KEYS = {
        "QB": _QB,
        "RB": _RUSH,
        "WR": _REC,
        "TE": _REC,
        "DEF": [],
    }

    def __init__(self, position: str, initial_value: int):
        self._position = position
        self._value = initial_value
        self._base_data = {
                "season_start_year": settings.CURRENT_YEAR,
                "day_of_week": "Sun",
                "game_date": date(2024, 12, 3),
                "game_week": 13,
                "opponent": "LAR",
                "pass_yds": 0,
                "pass_td": 0,
                "pass_attempts": 0,
                "pass_completions": 0,
                "interceptions": 0,
                "pass_completion_pct": 0,
                "pass_rating": 0,
                "rush_yds": 0,
                "rush_td": 0,
                "rush_attempts": 0,
                "targets": 0,
                "receptions": 0,
                "receiving_yards": 0,
                "receiving_td": 0
            }

    def __call__(self, *args, **kwargs):
        stats = {}
        keys = self.STAT_KEYS[self._position]
        for key in keys:
            mul = 1
            for mul, attrs in self._MODIFIERS.items():
                if key in attrs:
                    break
            stats[key] = self._value * mul

        self._base_data.update(stats)
        return self._base_data

