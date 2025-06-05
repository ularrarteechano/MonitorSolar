from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.dates import MonthArchiveView

from .models import Data
from kit.models import Kit
from .dates_utils import get_year_months, get_navigation

@method_decorator(login_required, name='dispatch')
class DataMonthTableView(MonthArchiveView):
    model = Data
    date_field = 'date'
    make_object_list = True
    month_format = "%m"
    allow_empty = True
    template_name = 'data/data_table.html'

    def get_queryset(self):
        kit_id = self.kwargs['kit_id']
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        return Data.objects.filter(kit_id=kit_id, kit__user=self.request.user, date__year=year, date__month=month)

    def dispatch(self, request, *args, **kwargs):
        self.kit_id = self.kwargs.get('kit_id')
        self.success_url = f'/kit/{self.kit_id}/'
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kit_id = self.kwargs.get('kit_id')
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['kit'] = get_object_or_404(Kit, id=kit_id, user=self.request.user)

        year_months = get_year_months(kit_id, Data)
        if year in year_months and month in year_months[year]:
            years, months_per_year, prev_year, prev_month, next_year, next_month = get_navigation(year_months, year, month)
        else:
            years, months_per_year, prev_year, prev_month, next_year, next_month = [], [], None, None, None, None

        context['years'] = years
        context['months_per_year'] = months_per_year
        context['prev_year'] = prev_year
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month
        context['year'] = year
        context['month'] = month
        return context