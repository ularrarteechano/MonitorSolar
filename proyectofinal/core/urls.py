from django.urls import path
from .views import HomeView, DashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]