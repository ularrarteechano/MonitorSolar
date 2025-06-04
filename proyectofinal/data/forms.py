from datetime import datetime
from django import forms
from .models import Data


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['date', 'yield_wh', 'consumption', 'max_power', 
                  'max_voltage', 'min_battery_voltage', 'max_battery_voltage', 
                  'bulk_time', 'absortion_time', 'float_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'yield_wh': forms.NumberInput(),
            'consumption': forms.NumberInput(),
            'max_power': forms.NumberInput(attrs={'step': '0.01'}),
            'max_voltage': forms.NumberInput(attrs={'step': '0.01'}),
            'min_battery_voltage': forms.NumberInput(attrs={'step': '0.01'}),
            'max_battery_voltage': forms.NumberInput(attrs={'step': '0.01'}),
            'bulk_time': forms.NumberInput(),
            'absortion_time': forms.NumberInput(),
            'float_time': forms.NumberInput()
        }  
        labels = {
            'date': 'Fecha',
            'yield_wh': 'Energía generada (Wh)',
            'consumption': 'Consumo (Wh)',
            'max_power': 'Potencia máxima (W)',
            'max_voltage': 'Voltaje máximo (V)',
            'min_battery_voltage': 'Voltaje mínimo de batería (V)',
            'max_battery_voltage': 'Voltaje máximo de batería (V)',
            'bulk_time': 'Bulk Time (minutos)',
            'absortion_time': 'Absorption Time (minutos)',
            'float_time': 'Float Time (minutos)'
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.now().date():
            raise forms.ValidationError("La fecha no puede ser futura.")
        return date

class DataFileForm(forms.Form):
    file = forms.FileField(label='Archivo CSV')
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('El archivo debe ser un CSV.')
        return file
    
class DataUpdateForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['date', 'yield_wh', 'consumption', 'max_power', 
                  'max_voltage', 'min_battery_voltage', 'max_battery_voltage', 
                  'bulk_time', 'absortion_time', 'float_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'readonly': True}, format='%Y-%m-%d'),
            'yield_wh': forms.NumberInput(),
            'consumption': forms.NumberInput(),
            'max_power': forms.NumberInput(attrs={'step': '0.01'}),
            'max_voltage': forms.NumberInput(attrs={'step': '0.01'}),
            'min_battery_voltage': forms.NumberInput(attrs={'step': '0.01'}),
            'max_battery_voltage': forms.NumberInput(attrs={'step': '0.01'}),
            'bulk_time': forms.NumberInput(),
            'absortion_time': forms.NumberInput(),
            'float_time': forms.NumberInput()
        }  
        labels = {
            'date': 'Fecha',
            'yield_wh': 'Energía generada (Wh)',
            'consumption': 'Consumo (Wh)',
            'max_power': 'Potencia máxima (W)',
            'max_voltage': 'Voltaje máximo (V)',
            'min_battery_voltage': 'Voltaje mínimo de batería (V)',
            'max_battery_voltage': 'Voltaje máximo de batería (V)',
            'bulk_time': 'Bulk Time (minutos)',
            'absortion_time': 'Absorption Time (minutos)',
            'float_time': 'Float Time (minutos)'
        }
        help_texts = {
            'date': 'La fecha del registro no es modificable.'
        }

class YearMonthForm(forms.Form):
    year = forms.IntegerField(label='Año', min_value=2000, max_value=datetime.now().year)
    month = forms.ChoiceField(label='Mes', choices=[(i, f'{i:02}') for i in range(1, 13)])
    
    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')
        
        if year is not None and month is not None:
            if datetime(year, int(month), 1) > datetime.now():
                raise forms.ValidationError("La fecha no puede ser futura.")
        return cleaned_data