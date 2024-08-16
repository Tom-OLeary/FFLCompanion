from rest_framework import status

from api.tests.util.fixtures import LEAGUE_SETTINGS, TEAM_OWNERS, FANTASY_TEAM_STATS, PLAYERS, ROSTERS, NFL_TEAMS
from api.tests.util.util import BaseTestCase
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.api_models.player import Player
from ffl_companion.api_models.roster import Roster
from owner.models import Owner


class TestLeagueLeadersView(BaseTestCase):
    # class attribute, model, fixtures
    IMPORT_DATA = [
        ("leagues", LeagueSettings, LEAGUE_SETTINGS),
        ("owners", Owner, TEAM_OWNERS),
        ("stats", FantasyTeamStats, FANTASY_TEAM_STATS),
        ("players", Player, PLAYERS),
        ("rosters", Roster, ROSTERS),
        ("nfl_teams", NFLTeam, NFL_TEAMS)
    ]

    nfl_teams: list[NFLTeam]
    roster: Roster = None
    league: LeagueSettings = None

    def generate_data(self):
        self.link_leagues()
        self.roster = self.query_model(Roster).get(roster_year=2024)
        self.league = self.query_model(LeagueSettings).get(setting_year=2024)
        self.roster.owner = self.user
        self.roster.league = self.league
        self.roster.save()

        for player, nfl_team in zip(self.players, self.nfl_teams):
            player.nfl_teams.add(nfl_team)

    def test_existing_roster_post_success(self):
        player_ids = [p.id for p in self.players]
        post_data = {
            "player_ids": ",".join([str(p) for p in player_ids]),
            "roster_id": self.roster.id
        }
        response = self.client.post("/api/rosters/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        expected_response = {
            "roster_year": 2024,
            "owner": self.user.id,
            "league": self.league.id,
        }
        for k, v in expected_response.items():
            self.assertEqual(results[k], v)

        players = results["players"]
        for p_id in player_ids:
            self.assertIn(p_id, players)

        self.assertTrue(self.user.rosters.count() == 1)
        self.assertTrue(self.user.rosters.first() == self.roster)

    def test_new_roster_post_success(self):
        # assert only 1 roster exists before creation
        self.assertTrue(len(self.rosters) == 1)

        player_ids = [p.id for p in self.players]
        post_data = {
            "player_ids": ",".join([str(p) for p in player_ids]),
            "roster_year": 2023
        }
        response = self.client.post("/api/rosters/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.query_model(Roster).count() == 2)

        results = response.json()
        expected_response = {
            "roster_year": 2023,
            "owner": self.user.id,
            "league": self.query_model(LeagueSettings).get(setting_year=2023).id,
        }
        for k, v in expected_response.items():
            self.assertEqual(results[k], v)

    def test_get_latest_roster_success(self):
        response = self.client.get("/api/rosters/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        expected_response = {
            "roster_year": 2024,
            "owner": self.user.id,
            "league": self.league.id,
            "players": [],
        }
        for k, v in expected_response.items():
            self.assertEqual(results[k], v)

    def test_get_latest_roster_none_existing_404(self):
        Roster.objects.all().delete()
        response = self.client.get("/api/rosters/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_roster_invalid_roster_id_404(self):
        non_existing_id = Roster.objects.order_by("id").last().id + 1
        post_data = {
            "roster_id": non_existing_id,
            "player_ids": "1,2,3"
        }
        response = self.client.post("/api/rosters/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["detail"], "No Roster matches the given query.")
