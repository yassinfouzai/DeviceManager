from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('log_in/', views.login_view, name='login'),
    path('log_out/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
