from collections import defaultdict
from datetime import datetime
import calendar

def get_labels_and_values(year, month, data_qs):
    """
    Devuelve dos listas:
    - labels: fechas del mes en formato YYYY-MM-DD (orden inverso)
    - values: yield_wh para cada fecha, 0 si no hay dato
    """
    num_days = calendar.monthrange(year, month)[1]
    all_days = [datetime(year, month, day).date() for day in range(1, num_days + 1)]
    all_days = list(reversed(all_days))
    data_dict = {d.date: d.yield_wh for d in data_qs}
    labels = [day.strftime('%Y-%m-%d') for day in all_days]
    values = [data_dict.get(day, 0) for day in all_days]
    return labels, values

def get_year_months(kit_id, DataModel):
    year_months = defaultdict(list)
    for y, m in DataModel.objects.filter(kit=kit_id)\
                                .values_list('date__year', 'date__month')\
                                .distinct()\
                                .order_by('date__year', 'date__month'):
        year_months[y].append(m)
    return year_months

def get_navigation(year_months, year, month):
    years = list(year_months.keys())
    months = list(year_months[year])
    year_index = years.index(year)
    month_index = months.index(month)

    # Anterior
    if month_index > 0:
        prev_year = year
        prev_month = months[month_index - 1]
    elif year_index > 0:
        prev_year = years[year_index - 1]
        prev_month = year_months[prev_year][-1]
    else:
        prev_year = None
        prev_month = None

    # Posterior
    if month_index < len(months) - 1:
        next_year = year
        next_month = months[month_index + 1]
    elif year_index < len(years) - 1:
        next_year = years[year_index + 1]
        next_month = year_months[next_year][0]
    else:
        next_year = None
        next_month = None

    return years, months, prev_year, prev_month, next_year, next_month