class ImmutableObjException(Exception):
    pass


class ConstantManager(object):
    """Handling of Immutable Constant Classes"""
    _instance: object = None
    _fields: tuple = None

    # allows IDE to recognize existing field choices
    # will only work if strings are explicitly listed per class and not dynamically generated
    __slots__: tuple = tuple()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # only need one instance of each class throughout project
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if self._fields is None or not self.__slots__:
            raise AttributeError(f"{self.__class__.__name__} has no fields")

        if len(self._fields) != len(self.__slots__):
            raise AttributeError(f"{self.__class__.__name__} must have same number of fields and __slots__")

        for key in zip(self.__slots__, self._fields):
            super().__setattr__(*key)

    def __setattr__(self, key, value):
        raise ImmutableObjException(f"Cannot change values of this class")

    @property
    def choices(self) -> list:
        # fallback if field choices are unclear
        return list(zip(self.__slots__, self._fields))


# ---------------- PLAYER ----------------
class PlayerOptions(ConstantManager):
    @classmethod
    def positions(cls) -> list[str]:
        return ["QB", "RB", "WR", "TE", "DEF"]


class PlayerBase(PlayerOptions):
    __slots__ = ("NAME", "POS")
    _fields = ("name", "position")


class PlayerStats(PlayerOptions):
    __slots__ = (
        "PASS_YDS",
        "PASS_TD",
        "PASS_ATTEMPTS",
        "PASS_COMPLETIONS",
        "INTERCEPTIONS",
        "PASS_COMPLETION_PCT",
        "PASS_RATING",
        "TARGETS",
        "RECEPTIONS",
        "RECEIVING_YDS",
        "RECEIVING_TD",
        "RUSH_YDS",
        "RUSH_TD",
        "RUSH_ATTEMPTS",
    )
    _fields = (
        "pass_yds",
        "pass_td",
        "pass_attempts",
        "pass_completions",
        "interceptions",
        "pass_completion_pct",
        "pass_rating",
        "targets",
        "receptions",
        "receiving_yards",
        "receiving_td",
        "rush_yds",
        "rush_td",
        "rush_attempts",
    )

    @property
    def passing(self) -> tuple:
        return (
            self.PASS_YDS,
            self.PASS_TD,
            self.PASS_ATTEMPTS,
            self.PASS_COMPLETIONS,
            self.INTERCEPTIONS,
            self.PASS_COMPLETION_PCT,
            self.PASS_RATING,
        )

    @property
    def receiving(self) -> tuple:
        return (
            self.TARGETS,
            self.RECEPTIONS,
            self.RECEIVING_YDS,
            self.RECEIVING_TD,
        )

    @property
    def rushing(self) -> tuple:
        return (
            self.RUSH_YDS,
            self.RUSH_TD,
            self.RUSH_ATTEMPTS,
        )


# ---------------- FANTASY TEAM ----------------
class FantasyStats(ConstantManager):
    __slots__ = (
        "OWNER",
        "OWNER_ID",
        "TEAM_NAME",
        "WINS",
        "LOSSES",
        "DRAWS",
        "TOTAL_POINTS",
        "TOTAL_POINTS_AGAINST",
        "PPG",
        "PAG",
        "NET_RATING",
        "REGULAR_SEASON_STANDING",
        "FINAL_SEASON_STANDING",
        "MADE_PLAYOFFS",
        "MADE_FINALS",
        "WON_FINALS",
        "ACQUISITIONS",
        "DROPS",
        "INJURED_RESERVE_COUNT",
        "MOVES",
        "TRADES",
        "SEASON_START_YEAR",
        "LEAGUE_NAME",
        "LEAGUE",
        "IS_CURRENT_SEASON",
    )
    _fields = (
        "owner",
        "owner_id",
        "team_name",
        "wins",
        "losses",
        "draws",
        "total_points",
        "total_points_against",
        "ppg",
        "pag",
        "net_rating",
        "regular_season_standing",
        "final_season_standing",
        "made_playoffs",
        "made_finals",
        "won_finals",
        "acquisitions",
        "drops",
        "injured_reserve_count",
        "moves",
        "trades",
        "season_start_year",
        "league_name",
        "league",
        "is_current_season",
    )
