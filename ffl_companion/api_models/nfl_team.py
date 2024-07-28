import pandas as pd
from django.db import models

from ffl_companion.api_models.base import BaseModelManager, BaseModel
from ffl_companion.api_models.choices import TeamChoices


class NFLTeamManager(BaseModelManager):
    KEY_MAPPING = {
        "Name": "name",
        "Abbreviation": "abbreviation",
        "Conference": "conference",
        "Division": "division",
    }

    def import_teams_csv(self, path: str):
        data = pd.read_csv(path).to_dict("records")

        to_import = []
        for d in data:
            d.pop("ID", None)
            team = {self.KEY_MAPPING[k]: v for k, v in d.items()}
            to_import.append(self.model(**team))

        self.bulk_create(to_import)


class NFLTeam(BaseModel):
    class Meta:
        db_table = "nfl_teams"
        unique_together = (("abbreviation", "season_year"),)

    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=3, choices=TeamChoices.choices)
    conference = models.CharField(max_length=3)
    division = models.CharField(max_length=4)
    season_year = models.IntegerField(default=2024)

    objects = NFLTeamManager()
