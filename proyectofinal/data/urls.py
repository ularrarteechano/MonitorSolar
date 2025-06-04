from django.urls import path
from .views import DataView, DataMonthTableView, DataMonthChartView, DataCreateView, DataCreateFromFileView, \
    DataUpdateView, DataDeleteView

urlpatterns = [
    path('', DataView.as_view(), name='data'),
    path('<int:kit_id>/table/<int:year>/<int:month>/', DataMonthTableView.as_view(), name='data_table'),
    path('<int:kit_id>/chart/<int:year>/<int:month>/', DataMonthChartView.as_view(), name='data_chart'),
    path('<int:kit_id>/add/', DataCreateView.as_view(), name='data_add'),
    path('<int:kit_id>/add/file', DataCreateFromFileView.as_view(), name='data_add_file'),
    path('<int:kit_id>/update/<int:data_id>', DataUpdateView.as_view(), name='data_update'),
    path('<int:kit_id>/delete/<int:data_id>', DataDeleteView.as_view(), name='data_delete')
]
