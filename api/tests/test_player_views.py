from rest_framework import status

from api.tests.util.fixtures import LEAGUE_SETTINGS, TEAM_OWNERS, PLAYERS, ROSTERS, NFL_TEAMS
from api.tests.util.util import BaseTestCase
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.api_models.player import Player
from ffl_companion.api_models.roster import Roster
from owner.models import Owner


class TestPlayerViews(BaseTestCase):
    # class attribute, model, fixtures
    IMPORT_DATA = [
        ("leagues", LeagueSettings, LEAGUE_SETTINGS),
        ("owners", Owner, TEAM_OWNERS),
        ("players", Player, PLAYERS),
        ("rosters", Roster, ROSTERS),
        ("nfl_teams", NFLTeam, NFL_TEAMS)
    ]

    nfl_teams: list[NFLTeam]
    roster: Roster = None
    league: LeagueSettings = None

    def test_get_latest_roster_success(self):
        unavailable1 = Player.objects.create(name="Player1", position="DEF")
        unavailable2 = Player.objects.create(name="Player2", position="RB")
        player_ids1 = [unavailable1.id, unavailable2.id]
        self.roster.players.set(player_ids1)

        roster2 = Roster.objects.create(dataset="testing", roster_year=2024)
        unavailable3 = Player.objects.create(name="Player3", position="DEF")
        unavailable4 = Player.objects.create(name="Player4", position="RB")
        player_ids2 = [unavailable3.id, unavailable4.id]
        roster2.players.set(player_ids2)

        unavailable_players = [unavailable1, unavailable2, unavailable3, unavailable4]

        # confirm unavailable players exist
        all_players = Player.objects.all()
        self.assertEqual(all_players.count(), 9)
        self.assertTrue(all(p in all_players for p in unavailable_players))

        # should only return available players
        response = self.client.get("/api/waivers/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.json()
        self.assertEqual(len(results), 5)
        result_ids = [row["id"] for row in results]
        for player in unavailable_players:
            self.assertNotIn(player.id, result_ids)
