from django.urls import re_path

from api.notifications.notification_views import NotificationAlertsView, NotificationUserView
from api.rosters.roster_views import RosterView, RosterDetailView, LatestRosterView, RosterBreakdownView
from api.trades.trade_views import TradesView
from api.leagues.league_views import LeagueSettingsView
from api.leaders.leader_views import LeagueLeadersView
from api.breakdowns.breakdown_views import LeagueBreakdownView, YearlyStatsView
from api.owners.owner_views import OwnerListView, OwnerDetailView
from api.players.player_views import ProjectionListView, PlayerDetailView, PlayerSearchView, WaiverView, PlayerStatsView
from api.trends.team_trend_views import TeamTrendView

urlpatterns = [
    re_path(r"^players/(?P<player_id>[0-9]+)/$", PlayerDetailView.as_view()),
    re_path(r"^projections/$", ProjectionListView.as_view()),
    re_path(r"^player-search/$", PlayerSearchView.as_view()),
    re_path(r"^player-stats/$", PlayerStatsView.as_view()),
    re_path(r"^owners/(?P<owner_id>[0-9]+)/$", OwnerDetailView.as_view()),
    re_path(r"^owners/$", OwnerListView.as_view()),
    re_path(r"^breakdown/$", LeagueBreakdownView.as_view()),
    re_path(r"^leaders/$", LeagueLeadersView.as_view()),
    re_path(r"^leagues/$", LeagueSettingsView.as_view()),
    re_path(r"^trades/$", TradesView.as_view()),
    re_path(r"^stats/$", YearlyStatsView.as_view()),
    re_path(r"^trends/$", TeamTrendView.as_view()),
    re_path(r"^rosters/(?P<roster_id>[0-9]+)/breakdown/$", RosterBreakdownView.as_view()),
    re_path(r"^rosters/(?P<roster_id>[0-9]+)/$", RosterDetailView.as_view()),
    re_path(r"^rosters/$", RosterView.as_view()),
    re_path(r"^rosters/user/$", LatestRosterView.as_view()),
    re_path(r"^notifications/(?P<owner_id>[0-9]+)/$", NotificationUserView.as_view()),
    re_path(r"^notifications/$", NotificationAlertsView.as_view()),
    re_path(r"^waivers/$", WaiverView.as_view()),
]
