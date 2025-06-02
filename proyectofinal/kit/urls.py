from django.urls import path
from .views import KitListView, KitCreateView, KitDetailView, \
    PanelCreateView, ControllerCreateView, KitUpdateView, \
    PanelUpdateView, ControllerUpdateView, KitDeleteView, \
    PanelDeleteView, ControllerDeleteView

urlpatterns = [
    path('', KitListView.as_view(), name='kit_list'),
    path('<int:kit_id>/', KitDetailView.as_view(), name='kit_detail'),
    path('create/', KitCreateView.as_view(), name='kit_create'),
    path('<int:kit_id>/update/', KitUpdateView.as_view(), name='kit_update'),
    path('<int:kit_id>/delete/', KitDeleteView.as_view(), name='kit_delete'),
    path('<int:kit_id>/panel/add/', PanelCreateView.as_view(), name='panel_add'),
    path('<int:kit_id>/panel/<int:panel_id>/update', PanelUpdateView.as_view(), name='panel_update'),
    path('<int:kit_id>/panel/<int:panel_id>/delete', PanelDeleteView.as_view(), name='panel_delete'),
    path('<int:kit_id>/controller/add/', ControllerCreateView.as_view(), name='controller_add'),
    path('<int:kit_id>/controller/<int:controller_id>/update', ControllerUpdateView.as_view(), name='controller_update'),
    path('<int:kit_id>/controller/<int:controller_id>/delete', ControllerDeleteView.as_view(), name='controller_delete')
]
