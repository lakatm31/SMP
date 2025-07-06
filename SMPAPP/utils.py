import math

def calculate_max_distance(power_kw, frequency_mhz, target_field_strength):
    power_w = power_kw * 1000  # kW → W

    # FM sáv
    if 87.5 <= frequency_mhz <= 108:
        distance_m = math.sqrt(30 * 1.65 * power_w) / target_field_strength
        method = "FM sáv – ESzCsM képlet"

    # VHF III (162–230 MHz)
    elif 162 <= frequency_mhz <= 230:
        distance_m = math.sqrt(30 * power_w) / target_field_strength
        method = "VHF III sáv – szabad tér modell"

    # DTV/UHF (470–860 MHz)
    elif 470 <= frequency_mhz <= 860:
        Pt_dBm = 10 * math.log10(power_w * 1000)  # W → mW → dBm
        Gt = 0  # dBi
        target_field_strength_dbuv = 20 * math.log10(target_field_strength) + 120
        num = Pt_dBm + Gt + 107 - target_field_strength_dbuv - 20 * math.log10(frequency_mhz) - 32.45
        d_km = 10 ** (num / 20)
        distance_m = d_km * 1000
        method = "DTV/UHF sáv – ITU-R P.1546 modell"

    # Egyéb sávok
    else:
        distance_m = 10 * math.sqrt(power_w)
        method = "Általános becslés"

    return {
        'max_distance_m': round(distance_m, 1),
        'target_field_strength_vpm': round(target_field_strength, 2),
        'method': method,
    }
