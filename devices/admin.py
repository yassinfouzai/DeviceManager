from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'location', 'creation_date')
    readonly_fields = ('creation_date',)
