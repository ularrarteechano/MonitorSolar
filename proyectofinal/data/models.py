from django.db import models
from kit.models import Kit


#Float model extend
class PositiveFloatField(models.FloatField):
    def __init__(self, *args, **kwargs):
        self.min_value = 0
        super(PositiveFloatField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value}
        defaults.update(kwargs)
        return super(PositiveFloatField, self).formfield(**defaults)
    
# Create your models here.
class Data(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name='date')
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, verbose_name='equipo solar', related_name='data')
    yield_wh = models.PositiveSmallIntegerField(verbose_name='yield(Wh)')
    consumption = models.PositiveSmallIntegerField(verbose_name='consumption(Wh)')
    max_power = PositiveFloatField(verbose_name='max. PV power(W)')
    max_voltage= PositiveFloatField(verbose_name='max. PV voltage(V)')
    min_battery_voltage = PositiveFloatField(verbose_name='min. battery voltage(V)')
    max_battery_voltage = PositiveFloatField(verbose_name='max. battery voltage(V)')
    bulk_time = models.PositiveSmallIntegerField(verbose_name='time in bulk(m)')
    absortion_time = models.PositiveSmallIntegerField(verbose_name='time in absorption(m)')
    float_time = models.PositiveSmallIntegerField(verbose_name='time in float(m)')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']