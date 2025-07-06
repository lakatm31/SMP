from django.contrib import admin
from .models import SimulationRecord

@admin.register(SimulationRecord)
class SimulationRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'frequency_mhz', 'power_kw', 'result_distance', 'method_used')
    list_filter = ('method_used', 'created_at')
    search_fields = ('user__username', 'method_used')