from django.db.models import Sum, Min, Max, Avg

from ffl_companion.constant_manager import PlayerBase, PlayerStats, FantasyStats

# Rounding
R2 = 2


# Enums
def enum(**enums):
    return type("Enum", (), enums)


FrameAgg = enum(
    SUM="sum",
    MIN="min",
    MAX="max",
    MEAN="mean",
    COUNT="count",
)


QueryAgg = enum(
    SUM=Sum,
    MIN=Min,
    MAX=Max,
    AVG=Avg,
)


PLAYER_BASE = PlayerBase()
PLAYER_STATS = PlayerStats()
FANTASY_TEAM_STATS = FantasyStats()
