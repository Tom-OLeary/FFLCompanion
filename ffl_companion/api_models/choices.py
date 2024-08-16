from django.db import models


class WeekdayChoices(models.TextChoices):
    MON = "Mon"
    TUE = "Tue"
    WED = "Wed"
    THU = "Thu"
    FRI = "Fri"
    SAT = "Sat"
    SUN = "Sun"


class TeamChoices(models.TextChoices):
    ARI = "ARI"
    ATL = "ATL"
    BAL = "BAL"
    BUF = "BUF"
    CAR = "CAR"
    CHI = "CHI"
    CIN = "CIN"
    CLE = "CLE"
    DAL = "DAL"
    DEN = "DEN"
    DET = "DET"
    GB = "GB"
    HOU = "HOU"
    IND = "IND"
    JAX = "JAX"
    KC = "KC"
    MIA = "MIA"
    MIN = "MIN"
    NE = "NE"
    NO = "NO"
    NYG = "NYG"
    NYJ = "NYJ"
    LV = "LV"
    PHI = "PHI"
    PIT = "PIT"
    LAC = "LAC"
    SF = "SF"
    SEA = "SEA"
    LAR = "LAR"
    TB = "TB"
    TEN = "TEN"
    WAS = "WAS"


class PositionChoices(models.TextChoices):
    QB = "QB"
    WR = "WR"
    RB = "RB"
    FB = "FB"
    TE = "TE"
    DEF = "DEF"
    K = "K"
    FLEX = "FLEX"

    @classmethod
    def default_lineup(cls):
        return [
            cls.QB.value,
            cls.RB.value,
            cls.RB.value,
            cls.WR.value,
            cls.WR.value,
            cls.TE.value,
            cls.FLEX.value,
            cls.DEF.value,
        ]

