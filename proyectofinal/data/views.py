import csv
from datetime import datetime
from io import TextIOWrapper

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView

from .forms import DataFileForm, DataForm, DataUpdateForm
from .models import Data
from kit.models import Kit

# Create your views here.
@method_decorator(login_required, name='dispatch')
class DataView(ListView):
    model = Kit
    template_name = 'data/data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kits'] = self.request.user.equipos_solares.all()
        context['year'] = datetime.now().year
        context['month'] = datetime.now().month
        return context

@method_decorator(login_required, name='dispatch')
class DataCreateView(CreateView):
    form_class= DataForm
    template_name = 'data/data_create.html'

    def get_queryset(self):
        kit_id = self.kwargs['kit_id']

    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        year = datetime.now().year
        month = datetime.now().month
        self.success_url = f'/data/{self.kit_id}/chart/{year}/{month}/'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kit_id = self.kwargs.get('kit_id')
        context['kit'] = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        return context

    def form_valid(self, form):
        kit_id = self.kwargs.get('kit_id')
        kit = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        data = form.save(commit=False)
        data.kit = kit
        if Data.objects.filter(kit=kit, date=data.date).exists():
            form.add_error('date', "Ya existe un registro para esta fecha. Si desea actualizarlo, use la opción de edición.")
            return self.form_invalid(form)
        data.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class DataCreateFromFileView(FormView):
    form_class= DataFileForm
    template_name = 'data/data_create_file.html'

    def get_queryset(self):
        kit_id = self.kwargs['kit_id']

    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        year = datetime.now().year
        month = datetime.now().month
        self.success_url = f'/data/{self.kit_id}/chart/{year}/{month}/'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kit_id = self.kwargs.get('kit_id')
        context['kit'] = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        return context
    
    def form_valid(self, form):
        kit = get_object_or_404(Kit, id=self.kit_id, user=self.request.user)
        csv_file = form.cleaned_data['file']
        csv_reader = csv.DictReader(TextIOWrapper(csv_file, encoding='utf-8'))

        required_fields = [
            'Date', 'Yield(Wh)', 'Consumption(Wh)', 'Max. PV power(W)', 'Max. PV voltage(V)',
            'Min. battery voltage(V)', 'Max. battery voltage(V)', 'Time in bulk(m)',
            'Time in absorption(m)', 'Time in float(m)'
        ]

        # 1. Verificar que todas las columnas requeridas existen
        missing_columns = [field for field in required_fields if field not in csv_reader.fieldnames]
        if missing_columns:
            form.add_error(None, f"Faltan las siguientes columnas en el archivo: {', '.join(missing_columns)}")
            return self.form_invalid(form)

        invalid_dates = []
        invalid_values = []

        for i, row in enumerate(csv_reader, start=2):  # start=2 para contar desde la primera fila de datos
            # 2. Revisar que la fecha sea correcta
            raw_date = row.get('Date', '')
            try:
                parsed_date = datetime.strptime(raw_date, "%m/%d/%y").date()
                if parsed_date > datetime.now().date():
                    raise ValueError("Fecha en el futuro")
            except Exception:
                invalid_dates.append(f"Fila {i}: '{raw_date}'")
                continue
            if Data.objects.filter(kit=kit, date=parsed_date).exists():
                # 3. Si el objeto Data ya existe, actualizarlo
                try:
                    Data.objects.filter(kit=kit, date=parsed_date).update(
                        yield_wh=row['Yield(Wh)'],
                        consumption=row['Consumption(Wh)'],
                        max_power=row['Max. PV power(W)'],
                        max_voltage=row['Max. PV voltage(V)'],
                        min_battery_voltage=row['Min. battery voltage(V)'],
                        max_battery_voltage=row['Max. battery voltage(V)'],
                        bulk_time=row['Time in bulk(m)'],
                        absortion_time=row['Time in absorption(m)'],
                        float_time=row['Time in float(m)']
                    )
                except Exception as e:
                    invalid_values.append(f"Fila {i}: {str(e)}")
                    continue
            else: 
                # 4. Intentar crear el objeto Data
                try:
                    Data.objects.create(
                        kit=kit,
                        date=parsed_date,
                        yield_wh=row['Yield(Wh)'],
                        consumption=row['Consumption(Wh)'],
                        max_power=row['Max. PV power(W)'],
                        max_voltage=row['Max. PV voltage(V)'],
                        min_battery_voltage=row['Min. battery voltage(V)'],
                        max_battery_voltage=row['Max. battery voltage(V)'],
                        bulk_time=row['Time in bulk(m)'],
                        absortion_time=row['Time in absorption(m)'],
                        float_time=row['Time in float(m)'],
                    )
                except Exception as e:
                    invalid_values.append(f"Fila {i}: {str(e)}")
                    continue

        errors = []
        if invalid_dates:
            errors.append("Fechas incorrectas: " + "; ".join(invalid_dates))
        if invalid_values:
            errors.append("Errores al guardar datos: " + "; ".join(invalid_values))

        if errors:
            form.add_error(None, " | ".join(errors))
            return self.form_invalid(form)

        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DataUpdateView(UpdateView):
    form_class = DataUpdateForm
    template_name = 'data/data_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Data, id=self.kwargs['data_id'], kit__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kit_id = self.kwargs.get('kit_id')
        context['year'] = self.request.GET.get('year') or datetime.now().year
        context['month'] = self.request.GET.get('month') or datetime.now().month
        context['kit'] = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        context['data'] = get_object_or_404(Data, id=self.kwargs.get('data_id'), kit__user=self.request.user)
        return context

    def get_success_url(self):
        year = self.request.GET.get('year') or datetime.now().year
        month = self.request.GET.get('month') or datetime.now().month
        return reverse('data_table', args=[self.kwargs['kit_id'], year, month])

    def form_valid(self, form):
        kit_id = self.kwargs.get('kit_id')
        kit = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        data = form.save(commit=False)
        data.kit = kit
        data.save()
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class DataDeleteView(DeleteView):
    model = Data
    template_name = 'data/data_delete.html'

    def get_object(self, queryset = ...):
        return get_object_or_404(Data, id=self.kwargs['data_id'], kit__user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        year = datetime.now().year
        month = datetime.now().month
        self.success_url = f'/data/{self.kit_id}/table/{year}/{month}/'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kit_id = self.kwargs.get('kit_id')
        context['year'] = datetime.now().year
        context['month'] = datetime.now().month
        context['kit'] = get_object_or_404(Kit, id=kit_id, user=self.request.user)
        context['data'] = get_object_or_404(Data, id=self.kwargs.get('data_id'), kit__user=self.request.user)
        return context