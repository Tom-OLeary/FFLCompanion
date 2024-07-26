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

    @property
    def trades(self):
        return [t[self] for t in [*self.owner_one_trades.all(), *self.owner_two_trades.all()]]
