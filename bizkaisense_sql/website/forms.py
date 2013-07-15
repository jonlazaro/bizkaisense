from django import forms
from django.forms.fields import DateField

from datetime import date, timedelta

OBSERVATION_TYPES = (
    ('so2', 'SO2'),
    ('no2', 'NO2'),
    ('pm10', 'PM10'),
    ('co', 'CO'),
    ('o3', 'O3'),
)
 
class heatmapForm(forms.Form):
    observationType = forms.ChoiceField(choices = OBSERVATION_TYPES)
    startDate = forms.fields.DateField(input_formats=('%Y-%m-%d',), widget=forms.DateInput(format='%Y-%m-%d'))
    endDate = forms.fields.DateField(input_formats=('%Y-%m-%d',), widget=forms.DateInput(format='%Y-%m-%d'))

class ObservationDetailsForm(forms.Form):
	date = forms.fields.DateField(input_formats=('%Y-%m-%d',), widget=forms.DateInput(format='%Y-%m-%d'))
	obstypes = forms.ChoiceField()

	def __init__(self, obstypes , *args, **kwargs):
		super(ObservationDetailsForm, self).__init__(*args, **kwargs)
		self.fields['obstypes'].choices = obstypes
