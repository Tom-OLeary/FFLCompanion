from rest_framework import status

from api.tests.fixtures import LEAGUE_SETTINGS, TEAM_OWNERS, FANTASY_TEAM_STATS
from api.tests.util import BaseTestCase
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.owner import TeamOwner
from ffl_companion.config import App


class TestLeagueLeadersView(BaseTestCase):
    # class attribute, model, fixtures
    IMPORT_DATA = [
        ("leagues", LeagueSettings, LEAGUE_SETTINGS),
        ("owners", TeamOwner, TEAM_OWNERS),
        ("stats", FantasyTeamStats, FANTASY_TEAM_STATS),
    ]

    leagues: list[LeagueSettings] = None
    owners: list[TeamOwner] = None
    stats: list[FantasyTeamStats] = None

    def setUp(self):
        self.assertTrue(App.config()["dataset"] == "testing")

        for league in self.leagues:
            year = league.setting_year
            FantasyTeamStats.objects.filter(season_start_year=year).update(league=league)

        for year in [2019, 2020, 2021, 2022, 2023]:
            stats = FantasyTeamStats.objects.filter(season_start_year=year).order_by("team_name")
            owners = TeamOwner.objects.order_by("name")
            for owner, stat in zip(owners, stats):
                stat.team_owner = owner
                stat.save()

    def test_league_leaders_view(self):
        response = self.client.get("/api/leaders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        titles = results["titles"]
        points = results["points"]
        wins = results["wins"]

        self.assertEqual(titles[0]["team_name"], "Team Name48")
        self.assertEqual(titles[0]["category"], "Titles")
        self.assertEqual(titles[0]["category_type"], "Total")

        self.assertEqual(points[0]["team_name"], "Team Name49")
        self.assertEqual(points[0]["category"], "Points")
        self.assertEqual(points[0]["category_type"], "Total")

        self.assertEqual(wins[0]["team_name"], "Team Name48")
        self.assertEqual(wins[0]["category"], "Wins")
        self.assertEqual(wins[0]["category_type"], "Total")

        # test ordering
        for rows in [titles, points, wins]:
            _current_row = rows[0]
            for row in rows:
                self.assertTrue(row["total"] <= _current_row["total"])
                _current_row = row
