from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

#ENUMS
class PanelType(models.TextChoices):
        MONOCRYSTALLINE = 'Monocristalino', 'Monocristalino'
        POLYCRYSTALLINE = 'Policristalino', 'Policristalino'
        AMORPHOUS = 'Amorfo', 'Amorfo'
        BIFACIAL = 'Bifacial', 'Bifacial'

class PanelVoltage(models.IntegerChoices):
        VOLTAGE_12 = 12, '12V'
        VOLTAGE_24 = 24, '24V'
        VOLTAGE_48 = 48, '48V'

class ChargeControllerType(models.TextChoices):
        PWM = 'PWM', 'PWM'
        MPPT = 'MPPT', 'MPPT'

# Create your models here.
class Kit(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=100, verbose_name='Nombre del equipo solar')
    active = models.BooleanField(default=True, verbose_name='Activo')
    installed = models.DateField(verbose_name='Fecha de instalación', default=now)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario', related_name='equipos_solares')

    class Meta:
        ordering = ['-active', '-installed']


class SolarPanel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    brand = models.CharField(max_length=100, verbose_name='Marca del panel')
    type = models.CharField(max_length=100, choices=PanelType.choices, verbose_name='Tipo de panel')
    watts = models.PositiveSmallIntegerField(verbose_name='Potencia del panel (W)')
    voltage = models.PositiveSmallIntegerField(choices=PanelVoltage.choices, verbose_name='Voltaje del panel (V)')
    serial_number = models.CharField(max_length=100, verbose_name='Número de serie del panel', null=True, blank=True)
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, verbose_name='Kit solar', related_name='solar_panels')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        ordering = ['-created']


class ChargeController(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    brand = models.CharField(max_length=100, verbose_name='Marca del regulador de carga')
    type = models.CharField(max_length=100, choices=ChargeControllerType.choices, verbose_name='Tipo de regulador de carga')
    max_voltage = models.PositiveSmallIntegerField(verbose_name='Voltaje máximo del regulador de carga (V)')
    max_amps = models.PositiveSmallIntegerField(verbose_name='Amperios máximos del regulador de carga (A)')
    serial_number = models.CharField(max_length=100, verbose_name='Número de serie del regulador de carga', null=True, blank=True)
    kit = models.OneToOneField(Kit, on_delete=models.CASCADE, verbose_name='Kit solar', related_name='charge_controller')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')


