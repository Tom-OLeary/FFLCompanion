from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ffl_companion.api_models.base import BaseModelManager, BaseModel
from ffl_companion.api_models.league_settings import LeagueSettings


class TeamOwnerManager(BaseModelManager):
    def create_owner(self, email=None, name=None, password=None, **extra_fields):
        now = timezone.now()
        if email:
            email = UserManager.normalize_email(email)

        owner = self.model(
            email=email,
            name=name,
            is_active=True,
            is_superuser=False,
            last_login=now,
            **extra_fields,
        )
        owner.set_password(password)
        owner.save(using=self._db)
        return owner

    def import_owners(self, owners: dict):
        to_import = []
        for owner, row in owners.items():
            print(f"ADDING {owner}")
            to_import.append(self.model(**row))

        self.bulk_create(to_import)


class TeamOwner(AbstractBaseUser, BaseModel):
    USERNAME_FIELD = "name"

    class Meta:
        db_table = "owners"
        unique_together = (("league_name", "name"),)

    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(null=True, blank=True)
    entry_year = models.IntegerField(null=True, blank=True)
    final_year = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    image = models.CharField(max_length=50, null=True, blank=True)
    league_name = models.CharField(max_length=50)
    password = models.CharField(_("password"), max_length=128, default="password")

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

    def set_password(self, password):
        self.password = make_password(password=password)
        self.save()

    def get_league_settings(self):
        league = LeagueSettings.objects.filter(name=self.league_name).first()
        if not league:
            raise AttributeError(f"{self.name} owner has no attribute 'league_name'")

        return {"name": league.name, "league_id": league.league_id}

