from django.urls import re_path

from api.trades.trade_views import TradesView
from api.leagues.league_views import LeagueSettingsView
from api.leaders.leader_views import LeagueLeadersView
from api.breakdowns.breakdown_views import LeagueBreakdownView, YearlyStatsView
from api.owners.owner_views import TeamOwnerListView, TeamOwnerDetailView
from api.players.player_views import PlayerListView, PlayerDetailView
from api.trends.team_trend_views import TeamTrendView

urlpatterns = [
    re_path(r"^players/$", PlayerListView.as_view()),
    re_path(r"^players/(?P<player_id>[0-9]+)/$", PlayerDetailView.as_view()),
    re_path(r"^owners/$", TeamOwnerListView.as_view()),
    re_path(r"^owners/(?P<owner_id>[0-9]+)/$", TeamOwnerDetailView.as_view()),
    re_path(r"^breakdown/$", LeagueBreakdownView.as_view()),
    re_path(r"^leaders/$", LeagueLeadersView.as_view()),
    re_path(r"^leagues/$", LeagueSettingsView.as_view()),
    re_path(r"^trades/$", TradesView.as_view()),
    re_path(r"^stats/$", YearlyStatsView.as_view()),
    re_path(r"^trends/$", TeamTrendView.as_view()),
]
