from django.db import models


class TeamOwnerManager(models.Manager):
    def import_owners(self, owners: dict):
        to_import = []
        for owner, row in owners.items():
            print(f"ADDING {owner}")
            to_import.append(self.model(**row))

        self.bulk_create(to_import)


class TeamOwner(models.Model):
    class Meta:
        db_table = "owners"
        unique_together = (("league_name", "name"),)

    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(null=True, blank=True)
    entry_year = models.IntegerField(null=True, blank=True)
    final_year = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    image = models.FilePathField(path="/img", null=True, blank=True)
    league_name = models.CharField(max_length=50)

    objects = TeamOwnerManager()

    @property
    def drafted_roster(self):
        return self.roster.all()

    @property
    def championships(self):
        return self.team_stats.filter(won_finals=True)

    @property
    def finals_appearances(self):
        return self.team_stats.filter(made_finals=True)

    @property
    def career_wins(self):
        return sum(s.wins for s in self.team_stats.all())

    @property
    def career_losses(self):
        return sum(s.losses for s in self.team_stats.all())


# owners = {
#     "Adam Barnes": {
#         "entry_year": 2009,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Adam Barnes",
#         "league_name": "Norton"
#     },
#     "Andrew Steele": {
#         "entry_year": 2018,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Andrew Steele",
#         "league_name": "Norton"
#     },
#     "Brandon cole, Michael Boyland": {
#         "entry_year": 2015,
#         "final_year": 2015,
#         "is_active": False,
#         "name": "Brandon cole, Michael Boyland",
#         "league_name": "Norton"
#     },
#     "Brian White": {
#         "entry_year": 2009,
#         "final_year": 2010,
#         "is_active": False,
#         "name": "Brian White",
#         "league_name": "Norton"
#     },
#     "Chris Preston": {
#         "entry_year": 2012,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Chris Preston",
#         "league_name": "Norton"
#     },
#     "Colin Ahern": {
#         "entry_year": 2018,
#         "final_year": 2018,
#         "is_active": False,
#         "name": "Colin Ahern",
#         "league_name": "Norton"
#     },
#     "Connor Sully": {
#         "entry_year": 2009,
#         "final_year": 2009,
#         "is_active": False,
#         "name": "Connor Sully",
#         "league_name": "Norton"
#     },
#     "Dylan LeVine": {
#         "entry_year": 2009,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Dylan LeVine",
#         "league_name": "Norton"
#     },
#     "Jake Pestana": {
#         "entry_year": 2009,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Jake Pestana",
#         "league_name": "Norton"
#     },
#     "Jake Scarafone": {
#         "entry_year": 2009,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Jake Scarafone",
#         "league_name": "Norton"
#     },
#     "Jarrod Church": {
#         "entry_year": 2014,
#         "final_year": 2014,
#         "is_active": False,
#         "name": "Jarrod Church",
#         "league_name": "Norton"
#     },
#     "Mike Clausen": {
#         "entry_year": 2014,
#         "final_year": 2017,
#         "is_active": False,
#         "name": "Mike Clausen",
#         "league_name": "Norton"
#     },
#     "Nick Martini": {
#         "entry_year": 2017,
#         "final_year": 2017,
#         "is_active": False,
#         "name": "Nick Martini",
#         "league_name": "Norton"
#     },
#     "Nigel Allard": {
#         "entry_year": 2009,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Nigel Allard",
#         "league_name": "Norton"
#     },
#     "Pat Plant": {
#         "entry_year": 2010,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Pat Plant",
#         "league_name": "Norton"
#     },
#     "Paul Southworth": {
#         "entry_year": 2009,
#         "final_year": 2011,
#         "is_active": False,
#         "name": "Paul Southworth",
#         "league_name": "Norton"
#     },
#     "REDACTED": {
#         "entry_year": 2017,
#         "final_year": 2023,
#         "is_active": False,
#         "name": "REDACTED",
#         "league_name": "Norton"
#     },
#     "Robert Allard": {
#         "entry_year": 2012,
#         "final_year": 2013,
#         "is_active": False,
#         "name": "Robert Allard",
#         "league_name": "Norton"
#     },
#     "Robert Southworth": {
#         "entry_year": 2009,
#         "final_year": 2011,
#         "is_active": False,
#         "name": "Robert Southworth",
#         "league_name": "Norton"
#     },
#     "Ryan Glynn": {
#         "entry_year": 2020,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Ryan Glynn",
#         "league_name": "Norton"
#     },
#     "Stephen Tessier": {
#         "entry_year": 2011,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Stephen Tessier",
#         "league_name": "Norton"
#     },
#     "Tom OLeary": {
#         "entry_year": 2009,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Tom OLeary",
#         "league_name": "Norton"
#     },
#     "Kevin Plant": {
#         "entry_year": 2024,
#         "final_year": 0,
#         "is_active": True,
#         "name": "Kevin Plant",
#         "league_name": "Norton"
#     }
# }
