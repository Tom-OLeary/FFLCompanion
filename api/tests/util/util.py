from collections import defaultdict

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

    @staticmethod
    def query_model(model):
        return model.objects.filter(dataset="testing")


def bulk_create(model, rows):
    to_create = [model(**r) for r in rows]
    return model.objects.bulk_create(to_create)
