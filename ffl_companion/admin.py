from django.contrib import admin

from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings, LeagueScoring
from ffl_companion.api_models.nfl_team import NFLTeam
from ffl_companion.api_models.player import NFLPlayer, Roster, Player, PlayerStatsWeekly
from ffl_companion.api_models.owner import TeamOwner

admin.site.register(NFLPlayer)
admin.site.register(TeamOwner)
admin.site.register(FantasyTeamStats)
admin.site.register(LeagueSettings)
admin.site.register(NFLTeam)
admin.site.register(LeagueScoring)
admin.site.register(Roster)
admin.site.register(Player)
admin.site.register(PlayerStatsWeekly)
