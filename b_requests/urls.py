from django.urls import path
from . import views


app_name = "requests"

urlpatterns = [
    path('borrow/<int:id>/', views.borrow_request_view, name='borrow-request'),
    path('return/<int:id>/', views.return_request_view, name='return-request'),
    path('approve/borrow/<int:pk>/', views.borrow_detail_view, name='borrow-detail'),
    path('approve/return/<int:pk>/', views.return_detail_view, name='return-detail'),
    path('', views.request_list_view, name='request-list'),
]
