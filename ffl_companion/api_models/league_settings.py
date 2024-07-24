from django.db import models


class LeagueSettings(models.Model):
    class Meta:
        db_table = "league_settings"
        unique_together = (("name", "setting_year"),)

    name = models.CharField(max_length=255, null=False)
    setting_year = models.IntegerField(null=False)
    playoff_teams = models.IntegerField(default=6)
    entry_price = models.IntegerField(default=0)
    member_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def prize_pool(self):
        return self.entry_price * self.member_count

    def save(self, *args, **kwargs):
        if not self.member_count:
            self.member_count = self.league_stats.count()

        super().save(*args, **kwargs)

