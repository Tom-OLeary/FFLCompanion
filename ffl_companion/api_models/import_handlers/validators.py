from dataclasses import dataclass, field

from ffl_companion.api_models.owner import TeamOwner


@dataclass
class FantasyTeamImport:
    is_final_standing: bool
    rank: int
    team: str
    record: str
    points_for: float
    points_against: float
    ppg: float
    pag: float
    diff: str

    team_name: str = field(init=False)
    owner_name: str = field(init=False)
    wins: int = field(init=False)
    losses: int = field(init=False)
    draws: int = field(init=False)
    ranking_type: str = field(init=False)

    def __post_init__(self):
        self.ranking_type = "final_season_standing" if self.is_final_standing else "regular_season_standing"
        # TODO TEMP
        if "(-.-)" in self.team:
            self.team_name = ",!,,(-.-),,!,"
            self.owner_name = "Tom OLeary"
        else:
            team_info = self.team.split("(")
            self.team_name = team_info[0].strip()
            self.owner_name = team_info[1].strip(")")

        self.wins, self.losses, self.draws = self.record.split("/")

    @property
    def data(self):
        return {
            self.ranking_type: self.rank,
            "team_owner": TeamOwner.objects.filter(name=self.owner_name).first(),
            "team_name": self.team_name,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "total_points": self.points_for,
            "total_points_against": self.points_against,
            "ppg": self.ppg,
            "pag": self.pag,
            "net_rating": self.diff,
        }
