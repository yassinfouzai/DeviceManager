from django.urls import path
from . import views

app_name = 'devices'

urlpatterns = [
    path('', views.device_list_view, name='device-list'),
    path('<int:id>/', views.device_detail_view, name='device-detail'),
]
