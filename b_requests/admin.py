from django.contrib import admin
from .models import BorrowRequest, ReturnRequest


# Register your models here.
admin.site.register(BorrowRequest)
admin.site.register(ReturnRequest)
