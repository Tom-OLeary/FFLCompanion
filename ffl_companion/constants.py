from django.db.models import Sum, Min, Max, Avg


# Rounding
R2 = 2


# Enums
def enum(**enums):
    # avoids requiring the additional call to '.value'
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

