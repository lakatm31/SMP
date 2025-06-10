import re
from django import forms

class TransmitterForm(forms.Form):
    latitude = forms.CharField(
        label="Latitude (Decimal or D°M'S\"N/S)",
        widget=forms.TextInput(attrs={'placeholder': '47°29\'52.5"N vagy 47.4979'})
    )
    longitude = forms.CharField(
        label="Longitude (Decimal or D°M'S\"E/W)",
        widget=forms.TextInput(attrs={'placeholder': '19°02\'24.0"E vagy 19.0400'})
    )
    power_kw = forms.FloatField(label="Power (kW)")
    frequency_mhz = forms.FloatField(label="Frequency (MHz)")
    target_field_strength = forms.FloatField(label="Target Field Strength (dBμV/m)")

    def clean_latitude(self):
        value = self.cleaned_data['latitude']
        return self._convert_dms_to_decimal(value)
    
    def clean_longitude(self):
        value = self.cleaned_data['longitude']
        return self._convert_dms_to_decimal(value)

    def _convert_dms_to_decimal(self, value):
        try:
            return float(value.replace(',', '.'))
        except ValueError:
            pass

        pattern = (
            r'^\s*(\d{1,3})°\s*(\d{1,2})[\'′]?\s*([\d\.,]+)?["″]?\s*([NSEWnsew])\s*$'
        )
        match = re.match(pattern, value.strip())
        if not match:
            raise forms.ValidationError(
                "Invalid coordinate format. Use decimal degrees or D°M'S\"N/S format."
            )

        degrees, minutes, seconds, direction = match.groups()
        decimal = int(degrees)
        if minutes:
            decimal += int(minutes) / 60
        if seconds:
            decimal += float(seconds.replace(',', '.')) / 3600

        if direction.upper() in ['S', 'W']:
            decimal = -decimal

        return decimal
