import math

def calculate_max_distance(power_kw, frequency_mhz, target_field_strength):
    power_w = power_kw * 1000

    if 87.5 <= frequency_mhz <= 108:
        # FM sáv – ESzCsM képlet
        distance_m = math.sqrt(30 * 1.65 * power_w) / 28
    else:
        # Általános becslés más sávokra – biztonságos fallback
        distance_m = 10 * math.sqrt(power_w)

    return {
        'max_distance_m': distance_m,
        'target_field_strength_dBuV_m': target_field_strength,
    }
