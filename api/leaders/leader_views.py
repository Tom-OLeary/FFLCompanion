from enum import Enum

import pandas as pd
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

from api.api_util import BaseAPIView
from api.decorators import require_token
from ffl_companion.constants import FrameAgg, enum, R2
from api.leaders.leader_serializers import LeagueLeaderSerializer
from ffl_companion.api_models.fantasy_tracker import FantasyTeamStats


GENERATE_LEADER = "_generate_leader"
GENERATE_MAX_TOTAL = "_generate_max_total"
OWNER_ID = "owner_id"
YEARS_COUNT = "years_count"


OperationKey = enum(
    WON_FINALS="won_finals",
    MADE_PLAYOFFS="made_playoffs",
    MADE_FINALS="made_finals",
    TOTAL_POINTS="total_points",
    WINS="wins",
    PPG="ppg",
)


CategoryKey = enum(
    TITLES_SUM="titles_sum",
    POINTS_YR="points_yr",
    WINS_YR="wins_yr",
    TOTAL_POINTS="total_points",
    WINS="wins",
    PPG_YR="ppg_yr",
    PLAYOFF_APP="playoff_appearances",
    FINALS_APP="finals_appearances",
    PLAYOFF_RATE="playoff_rate",
)


class OutputKey(Enum):
    # Response Serializer Fields
    titles = (CategoryKey.TITLES_SUM, GENERATE_LEADER)
    playoffs = (CategoryKey.PLAYOFF_APP, GENERATE_LEADER)
    finals = (CategoryKey.FINALS_APP, GENERATE_LEADER)
    points = (CategoryKey.POINTS_YR, GENERATE_LEADER)
    wins = (CategoryKey.WINS_YR, GENERATE_LEADER)
    ppg = (CategoryKey.PPG_YR, GENERATE_LEADER)
    playoff_rate = (CategoryKey.PLAYOFF_RATE, GENERATE_LEADER)
    # -------------- max totals, these results rely upon the specific row the data comes from
    points_max = (CategoryKey.TOTAL_POINTS, GENERATE_MAX_TOTAL)
    wins_max = (CategoryKey.WINS, GENERATE_MAX_TOTAL)


class LeagueLeadersView(BaseAPIView):
    model = FantasyTeamStats

    CATEGORY_MAP = {
        # Leaderboard Display Titles
        CategoryKey.TITLES_SUM: ("Total", "Titles"),
        CategoryKey.POINTS_YR: ("Avg", "Points"),
        CategoryKey.WINS_YR: ("Avg", "Wins"),
        CategoryKey.TOTAL_POINTS: ("Total", "Points"),
        CategoryKey.WINS: ("Total", "Wins"),
        CategoryKey.PPG_YR: ("Avg", "PPG"),
        CategoryKey.PLAYOFF_APP: ("Total", "Playoffs"),
        CategoryKey.FINALS_APP: ("Total", "Finals"),
        CategoryKey.PLAYOFF_RATE: ("Rate", "Playoffs"),
    }

    OPERATION_MAP = {
        CategoryKey.TITLES_SUM: (OperationKey.WON_FINALS, FrameAgg.SUM),
        CategoryKey.PLAYOFF_APP: (OperationKey.MADE_PLAYOFFS, FrameAgg.SUM),
        CategoryKey.FINALS_APP: (OperationKey.MADE_FINALS, FrameAgg.SUM),
        CategoryKey.POINTS_YR: (OperationKey.TOTAL_POINTS, FrameAgg.MEAN),
        CategoryKey.WINS_YR: (OperationKey.WINS, FrameAgg.MEAN),
        CategoryKey.PPG_YR: (OperationKey.PPG, FrameAgg.MEAN),
        CategoryKey.PLAYOFF_RATE: (OperationKey.MADE_PLAYOFFS, FrameAgg.MEAN),
    }

    QUERY_VALUES = [
        "owner_id",
        "wins",
        "total_points",
        "ppg",
        "net_rating",
        "won_finals",
        "made_playoffs",
        "made_finals",
        "season_start_year",
        "team_name",
        "name",
        "is_active",
        "image",
    ]

    def _generate_leader(self, rank_df: pd.DataFrame, key: str):
        group_key, operation = self.OPERATION_MAP[key]
        rank_df[key] = rank_df.groupby(OWNER_ID)[group_key].transform(operation).round(R2)
        rank_df.sort_values(by=[key, OWNER_ID, "season_start_year"], inplace=True, ascending=False)
        return rank_df

    @staticmethod
    def _generate_max_total(df: pd.DataFrame, key: str):
        _idx = df.groupby(OWNER_ID)[key].transform(FrameAgg.MAX) == df[key]
        return df[_idx].sort_values(by=[key, YEARS_COUNT], ascending=False).round(R2)

    def _generate_rank(self, df: pd.DataFrame, key: str, func: str):
        if df.empty:
            return []

        rank_df = df.copy()
        rank_df["category_type"], rank_df["category"] = self.CATEGORY_MAP[key]
        rank_df = getattr(self, func)(rank_df, key).drop_duplicates(subset=[OWNER_ID, key], keep="first").rename(columns={key: "total"})
        return rank_df.to_dict("records")

    @require_token
    def get(self, request):
        stats = self.get_queryset().select_related("owner").annotate(
            name=F("owner__name"),
            is_active=F("owner__is_active"),
            image=F("owner__image")
        ).values(*self.QUERY_VALUES)
        if not stats:
            return Response([], status=status.HTTP_200_OK)

        stats_df = pd.DataFrame(stats)
        stats_df[YEARS_COUNT] = stats_df.groupby(OWNER_ID)[OWNER_ID].transform(FrameAgg.COUNT)
        stats_df.fillna(0, inplace=True)

        serializer = LeagueLeaderSerializer({k.name: self._generate_rank(stats_df, *k.value) for k in OutputKey})
        return Response(serializer.data, status=status.HTTP_200_OK)
