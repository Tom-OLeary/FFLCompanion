from typing import Type

import pandas as pd

from ffl_companion.constants import FrameAgg, enum, R2

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


OutputKey = enum(
    # Response Serializer Fields
    TITLES="titles",
    PLAYOFFS="playoffs",
    FINALS= "finals",
    POINTS="points",
    WINS="wins",
    PPG="ppg",
    PLAYOFF_RATE="playoff_rate",
    # -------------- max totals, these results rely upon the specific row the data comes from
    POINTS_MAX="points_max",
    WINS_MAX="wins_max",
)


class LeaderRankingException(Exception):
    pass


class GenerateLeader:
    METHODS = enum(
        ALL_TIME="_generate_all_time_leader",
        YEAR_SPECIFIC="_generate_year_specific_leader",
    )

    CATEGORY_TYPE: str = None  # Title displayed on Leaderboard
    CATEGORY: str = None  # Category displayed on Leaderboard

    CATEGORY_KEY: CategoryKey = None
    METHOD: str = None
    OPERATION: FrameAgg = None
    GROUP_KEY: OperationKey = None
    OUTPUT_KEY: OutputKey = None

    def __init__(self, stats_df: pd.DataFrame):
        if not all([self.CATEGORY_KEY, self.CATEGORY_TYPE, self.CATEGORY, self.OUTPUT_KEY]):
            raise LeaderRankingException(f"Subclass must implement all attributes")

        self._stats_df = stats_df.copy()
        self._init_dataframe()

    def _init_dataframe(self):
        self._stats_df[YEARS_COUNT] = self._stats_df.groupby(OWNER_ID)[OWNER_ID].transform(FrameAgg.COUNT)
        self._stats_df.fillna(0, inplace=True)
        self._stats_df["category_type"], self._stats_df["category"] = self.CATEGORY_TYPE, self.CATEGORY

    def generate(self) -> list[dict]:
        if self._stats_df.empty:
            return []

        getattr(self, self.METHOD)()
        return (
            self._stats_df.drop_duplicates(
                subset=[OWNER_ID, self.CATEGORY_KEY],
                keep="first"
            )
            .rename(columns={self.CATEGORY_KEY: "total"})
            .to_dict("records")
        )

    def _generate_all_time_leader(self):
        """Generates leaders as an aggregation of all-time stats"""
        if not all([self.GROUP_KEY, self.OPERATION]):
            raise LeaderRankingException(f"Subclass Missing One or More Operation Attributes")

        self._stats_df[self.CATEGORY_KEY] = self._stats_df.groupby(OWNER_ID)[self.GROUP_KEY].transform(self.OPERATION).round(R2)
        self._stats_df.sort_values(by=[self.CATEGORY_KEY, OWNER_ID, "season_start_year"], inplace=True, ascending=False)

    def _generate_year_specific_leader(self):
        """
        Generates leaders where values tie-in to a specific year (i.e. most points in season).
        Used to gather other relevant data from that year such as team name, year, etc...
        """
        _idx = self._stats_df.groupby(OWNER_ID)[self.CATEGORY_KEY].transform(FrameAgg.MAX) == self._stats_df[self.CATEGORY_KEY]
        self._stats_df = self._stats_df[_idx].sort_values(by=[self.CATEGORY_KEY, YEARS_COUNT], ascending=False).round(R2)


class TotalTitles(GenerateLeader):
    CATEGORY_TYPE = "Total"
    CATEGORY = "Titles"
    CATEGORY_KEY = CategoryKey.TITLES_SUM
    METHOD = GenerateLeader.METHODS.ALL_TIME
    OPERATION = FrameAgg.SUM
    GROUP_KEY = OperationKey.WON_FINALS
    OUTPUT_KEY = OutputKey.TITLES


class AvgPoints(GenerateLeader):
    CATEGORY_TYPE = "Avg"
    CATEGORY = "Points"
    CATEGORY_KEY = CategoryKey.POINTS_YR
    METHOD = GenerateLeader.METHODS.ALL_TIME
    OPERATION = FrameAgg.MEAN
    GROUP_KEY = OperationKey.TOTAL_POINTS
    OUTPUT_KEY = OutputKey.POINTS


class AvgWins(GenerateLeader):
    CATEGORY_TYPE = "Avg"
    CATEGORY = "Wins"
    CATEGORY_KEY = CategoryKey.WINS_YR
    METHOD = GenerateLeader.METHODS.ALL_TIME
    OPERATION = FrameAgg.MEAN
    GROUP_KEY = OperationKey.WINS
    OUTPUT_KEY = OutputKey.WINS


class AvgPPG(GenerateLeader):
    CATEGORY_TYPE = "Avg"
    CATEGORY = "PPG"
    CATEGORY_KEY = CategoryKey.PPG_YR
    METHOD = GenerateLeader.METHODS.ALL_TIME
    OPERATION = FrameAgg.MEAN
    GROUP_KEY = OperationKey.PPG
    OUTPUT_KEY = OutputKey.PPG


class TotalPlayoffs(GenerateLeader):
    CATEGORY_TYPE = "Total"
    CATEGORY = "Playoffs"
    CATEGORY_KEY = CategoryKey.PLAYOFF_APP
    METHOD = GenerateLeader.METHODS.ALL_TIME
    OPERATION = FrameAgg.SUM
    GROUP_KEY = OperationKey.MADE_PLAYOFFS
    OUTPUT_KEY = OutputKey.PLAYOFFS


class TotalFinals(GenerateLeader):
    CATEGORY_TYPE = "Total"
    CATEGORY = "Finals"
    CATEGORY_KEY = CategoryKey.FINALS_APP
    METHOD = GenerateLeader.METHODS.ALL_TIME
    OPERATION = FrameAgg.SUM
    GROUP_KEY = OperationKey.MADE_FINALS
    OUTPUT_KEY = OutputKey.FINALS


class PlayoffRate(GenerateLeader):
    CATEGORY_TYPE = "Rate"
    CATEGORY = "Playoffs"
    CATEGORY_KEY = CategoryKey.PLAYOFF_RATE
    METHOD = GenerateLeader.METHODS.ALL_TIME
    OPERATION = FrameAgg.MEAN
    GROUP_KEY = OperationKey.MADE_PLAYOFFS
    OUTPUT_KEY = OutputKey.PLAYOFF_RATE


class MaxPoints(GenerateLeader):
    CATEGORY_TYPE = "Total"
    CATEGORY = "Points"
    CATEGORY_KEY = CategoryKey.TOTAL_POINTS
    METHOD = GenerateLeader.METHODS.YEAR_SPECIFIC
    OUTPUT_KEY = OutputKey.POINTS_MAX


class MaxWins(GenerateLeader):
    CATEGORY_TYPE = "Total"
    CATEGORY = "Wins"
    CATEGORY_KEY = CategoryKey.WINS
    METHOD = GenerateLeader.METHODS.YEAR_SPECIFIC
    OUTPUT_KEY = OutputKey.WINS_MAX


class Rank:
    def __init__(self, stats_df: pd.DataFrame):
        self._stats_df = stats_df
        self._categories = []

    def run(self):
        return {c.OUTPUT_KEY: c.generate() for c in self._categories}

    def register(self, category: Type[GenerateLeader]):
        self._categories.append(category(self._stats_df))
