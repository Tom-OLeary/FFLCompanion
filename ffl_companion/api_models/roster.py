from django.core.validators import MaxValueValidator
from django.db import models

from ffl_companion.api_models.base import BaseModel, BaseModelManager
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.api_models.player import Player
from owner.models import Owner


class RosterLimitException(Exception):
    pass


class RosterModelManager(BaseModelManager):
    pass


class Roster(BaseModel):
    class Meta:
        db_table = "rosters"
        unique_together = (("owner", "roster_year"),)

    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name="rosters")
    players = models.ManyToManyField(Player, related_name="player_rosters")
    roster_year = models.IntegerField(default=2024)
    league = models.ForeignKey(LeagueSettings, on_delete=models.SET_NULL, null=True, related_name="settings_rosters")

    objects = RosterModelManager()

    @property
    def player_limit(self):
        return self.league.player_limit

    @property
    def lineup_positions(self):
        try:
            return self.league.lineup_positions.split(",")
        except AttributeError:
            self.league.save()  # will set default lineup
            return self.league.lineup_positions.split(",")


class Lineup(BaseModel):
    class Meta:
        db_table = "lineups"
        unique_together = (("roster", "week"),)

    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name="lineups")
    week = models.IntegerField(default=1, validators=[MaxValueValidator(18)])
    starters = models.ManyToManyField(Player, related_name="starters")
    bench = models.ManyToManyField(Player, related_name="bench_players")

    @property
    def starting_lineup_positions(self):
        return [pos for pos in self.roster.lineup_positions if pos != "BE"]

    def set_starters(self, players: list[Player], flex_player: Player = None, defense: NFLTeam = None):
        _positions = self.starting_lineup_positions
        if len(players) > len(_positions) - 1:  # - 1 for defense
            raise RosterLimitException("Players exceed starting lineup total")

        for player in players:
            if player == flex_player:
                continue
            try:
                _positions.remove(player.position)
            except ValueError:
                raise RosterLimitException(f"Player Positions exceed starting lineup total: {player.name}, {player.position}")

        self.starters.set(players)
        if defense:
            #  TODO create Player records for nfl teams and treat them as defense players
            self.starters.add(defense)
