from rest_framework import status

from api.tests.util.fixtures import LEAGUE_SETTINGS, TEAM_OWNERS, FANTASY_TEAM_STATS, PLAYERS, ROSTERS, NFL_TEAMS
from api.tests.util.util import BaseTestCase
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.api_models.player import Player
from ffl_companion.api_models.roster import Roster
from owner.models import Owner


class TestRosterViews(BaseTestCase):
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
        super().generate_data()
        for player, nfl_team in zip(self.players, self.nfl_teams):
            player.nfl_teams.add(nfl_team)

    def test_new_roster_post_success(self):
        Roster.objects.all().delete()
        player_ids = [p.id for p in self.players]
        post_data = {"player_ids": [p for p in player_ids]}
        response = self.client.post("/api/rosters/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.query_model(Roster).count() == 1)

        results = response.json()
        self.assertTrue(results == "ok")

    def test_get_latest_roster_success(self):
        response = self.client.get("/api/rosters/user/?latest=true", format="json")
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

    def test_get_latest_roster_none_existing(self):
        Roster.objects.all().delete()
        response = self.client.get("/api/rosters/user/?latest=true", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    def test_delete_roster_success(self):
        self.assertEqual(Roster.objects.count(), 1)
        response = self.client.delete(f"/api/rosters/{self.roster.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "deleted")
        self.assertEqual(Roster.objects.count(), 0)

    def test_update_roster_add_players_success(self):
        new_player1 = Player.objects.create(name="NP1", position="QB")
        new_player2 = Player.objects.create(name="NP2", position="RB")
        player_add_ids = [new_player1.id, new_player2.id]
        post_data = {"player_add_ids": player_add_ids}

        self.assertEqual(self.roster.players.count(), 0)
        response = self.client.post(f"/api/rosters/{self.roster.id}/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.roster.players.count(), 2)

        expected_response = {
            "NP1": "QB",
            "NP2": "RB",
        }
        for player in self.roster.players.all():
            self.assertEqual(expected_response[player.name], player.position)

    def test_update_roster_drop_players_success(self):
        existing_player1 = Player.objects.create(name="EP1", position="QB")
        existing_player2 = Player.objects.create(name="EP2", position="RB")
        player_ids = [existing_player1.id, existing_player2.id]
        self.roster.players.set(player_ids)
        self.assertEqual(self.roster.players.count(), 2)

        post_data = {"player_drop_ids": [existing_player1.id]}
        response = self.client.post(f"/api/rosters/{self.roster.id}/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.roster.players.count(), 1)

        player = self.roster.players.first()
        self.assertEqual(player.name, existing_player2.name)
        self.assertEqual(player.position, existing_player2.position)

    def test_update_roster_mixed_players_success(self):
        existing_player1 = Player.objects.create(name="EP1", position="DEF")
        existing_player2 = Player.objects.create(name="EP2", position="RB")
        player_ids = [existing_player1.id, existing_player2.id]
        self.roster.players.set(player_ids)
        self.assertEqual(self.roster.players.count(), 2)

        new_player1 = Player.objects.create(name="NP1", position="WR")
        new_player2 = Player.objects.create(name="NP2", position="TE")

        # drop existing_player1, add new_player1, new_player2
        post_data = {
            "player_add_ids": [new_player1.id, new_player2.id],
            "player_drop_ids": [existing_player1.id],
        }
        response = self.client.post(f"/api/rosters/{self.roster.id}/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.roster.players.count(), 3)

        expected_response = {
            "EP2": "RB",
            "NP1": "WR",
            "NP2": "TE",
        }
        for player in self.roster.players.all():
            self.assertEqual(expected_response[player.name], player.position)

    def test_400_player_not_available(self):
        existing_player1 = Player.objects.create(name="EP1", position="DEF")
        existing_player2 = Player.objects.create(name="EP2", position="RB")
        player_ids = [existing_player1.id, existing_player2.id]
        self.roster.players.set(player_ids)

        roster2 = Roster.objects.create(dataset="testing", roster_year=2024)
        post_data = {"player_add_ids": [existing_player1.id]}
        response = self.client.post(f"/api/rosters/{roster2.id}/", data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), "One or more players not available")

    def test_roster_breakdown_response(self):
        self.generate_rosters()
        self.roster.players.set(self.players)  # user roster

        response = self.client.get(f"/api/rosters/{self.roster.id}/breakdown/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        print("------------", results)
