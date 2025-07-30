from django.contrib import admin
from .models import BorrowRequest, ReturnRequest


admin.site.register(BorrowRequest)


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'device', 'date_returned', 'review')
    readonly_fields = ('date_returned',)

