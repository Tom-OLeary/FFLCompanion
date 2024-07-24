from django.contrib import admin

from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats
from ffl_companion.api_models.league_settings import LeagueSettings
from ffl_companion.api_models.player import NFLPlayer
from ffl_companion.api_models.owner import TeamOwner

admin.site.register(NFLPlayer)
admin.site.register(TeamOwner)
admin.site.register(FantasyTeamStats)
admin.site.register(LeagueSettings)
