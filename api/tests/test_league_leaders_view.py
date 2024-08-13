from rest_framework import status

from api.tests.util.fixtures import LEAGUE_SETTINGS, TEAM_OWNERS, FANTASY_TEAM_STATS
from api.tests.util.util import BaseTestCase
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from owner.models import Owner


class TestLeagueLeadersView(BaseTestCase):
    # class attribute, model, fixtures
    IMPORT_DATA = [
        ("leagues", LeagueSettings, LEAGUE_SETTINGS),
        ("owners", Owner, TEAM_OWNERS),
        ("stats", FantasyTeamStats, FANTASY_TEAM_STATS),
    ]

    leagues: list[LeagueSettings] = None
    owners: list[Owner] = None
    stats: list[FantasyTeamStats] = None

    def generate_data(self):
        self.link_leagues()

    def test_league_leaders_view(self):
        response = self.client.get("/api/leaders/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        titles = results["titles"]
        points = results["points"]
        wins = results["wins"]

        # TODO update for team_name
        # self.assertEqual(titles[0]["team_name"], "Team Name48")
        self.assertEqual(titles[0]["category"], "Titles")

        # self.assertEqual(points[0]["team_name"], "Team Name49")
        self.assertEqual(points[0]["category"], "Points")

        # self.assertEqual(wins[0]["team_name"], "Team Name48")
        self.assertEqual(wins[0]["category"], "Wins")

        # test ordering and category_type
        for rows in [titles, points, wins]:
            _current_row = rows[0]
            for row in rows:
                # self.assertEqual(row["category_type"], "Total")
                self.assertTrue(row["total"] <= _current_row["total"])
                _current_row = row
