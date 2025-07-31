from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('main.urls')),
    path('devices/', include('devices.urls', namespace='devices')),
    path('requests/', include('b_requests.urls', namespace='requests')),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
