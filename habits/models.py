from django.db import models
from django.conf import settings


class Cadence(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"


class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=120)
    description= models.TextField(blank=True)
    cadence = models.CharField(max_length=10, choices=Cadence.choices, default=Cadence.DAILY)
    target_per_period = models.PositiveBigIntegerField(default=1)
    color =  models.CharField(max_length=7, default="9ece6a")
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["owner", "is_archived"])]
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="uniq_habit_name_per_owner")
        ]

        def __str__(self) -> str:
            return f"{self.name} ({self.owner_id})"

class CheckIn(models.Model):
    habit   = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="checkins")
    done_at = models.DateField()
    note    = models.TextField(blank=True)
    value   = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["habit", "done_at"], name="one_checkin_per_day"),
        ]