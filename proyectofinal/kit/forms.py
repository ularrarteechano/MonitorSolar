from datetime import datetime
from django import forms
from django.utils.timezone import now
from .models import Kit, SolarPanel, ChargeController, PanelType, ChargeControllerType, PanelVoltage


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ['name', 'active', 'installed']
        widgets = {
            'name': forms.TextInput(),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'installed': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        labels = {
            'name': 'Nombre del equipo solar',
            'active': 'Activo',
            'installed': 'Fecha de instalación'
        }

    def clean_installed(self):
        date = self.cleaned_data['installed']
        if date > datetime.now().date():
            raise forms.ValidationError("La fecha no puede ser futura.")
        return date

class PanelForm(forms.ModelForm):
    class Meta:
        model = SolarPanel
        fields = ['brand', 'type', 'watts', 'voltage', 'serial_number']
        widgets = {
            'brand': forms.TextInput(),
            'type': forms.Select(choices=PanelType.choices),
            'watts': forms.NumberInput(),
            'voltage': forms.Select(choices=PanelVoltage.choices),
            'serial_number': forms.TextInput()
        }
        labels = {
            'brand': 'Marca del panel',
            'type': 'Tipo de panel',
            'watts': 'Potencia del panel (W)',
            'voltage': 'Voltaje del panel (V)',
            'serial_number': 'Número de serie del panel'
        }
        help_texts = {
            'serial_number': '*Opcional'
        }

class ControllerForm(forms.ModelForm):
    class Meta:
        model = ChargeController
        fields = ['brand', 'type', 'max_voltage', 'max_amps', 'serial_number']
        widgets = {
            'brand': forms.TextInput(),
            'type': forms.Select(choices =ChargeControllerType.choices),
            'max_voltage': forms.NumberInput(),
            'max_amps': forms.NumberInput(),
            'serial_number': forms.TextInput()
        }
        labels = {
            'brand': 'Marca del regulador de carga',
            'type': 'Tipo de regulador de carga',
            'max_voltage': 'Voltaje máximo del regulador de carga (V)',
            'max_amps': 'Amperios máximos del regulador de carga (A)',
            'serial_number': 'Número de serie del regulador de carga'
        }
        help_texts = {
            'serial_number': '*Opcional'
        }