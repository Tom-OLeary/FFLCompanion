from django.urls import re_path

from api.fantasy_tracker.nfl_views import PlayerListView, PlayerDetailView, TeamOwnerListView, TeamOwnerDetailView, \
    LeagueBreakdownView, LeagueLeadersView, LeagueSettingsView, TradesView

urlpatterns = [
    re_path(r"^players/$", PlayerListView.as_view()),
    re_path(r"^players/(?P<player_id>[0-9]+)/$", PlayerDetailView.as_view()),
    re_path(r"^owners/$", TeamOwnerListView.as_view()),
    re_path(r"^owners/(?P<owner_id>[0-9]+)/$", TeamOwnerDetailView.as_view()),
    re_path(r"^breakdown/$", LeagueBreakdownView.as_view()),
    re_path(r"^leaders/$", LeagueLeadersView.as_view()),
    re_path(r"^leagues/$", LeagueSettingsView.as_view()),
    # re_path(r"^leagues/(?P<league_id>[0-9]+)/$", TeamOwnerDetailView.as_view()),
    re_path(r"^trades/$", TradesView.as_view()),

]
