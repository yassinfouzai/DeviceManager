from django.urls import path
from .views import home_view, dashboard_view


urlpatterns = [
    path('', home_view, name="home"),
    path('dashboard/', dashboard_view, name='dashboard'),
]
