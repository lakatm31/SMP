
from django.db import models
from django.contrib.auth.models import User

class SimulationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    power_kw = models.FloatField()
    frequency_mhz = models.FloatField()
    target_field_strength = models.FloatField()
    result_distance = models.FloatField()
    method_used = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.created_at.strftime('%Y-%m-%d %H:%M')}"