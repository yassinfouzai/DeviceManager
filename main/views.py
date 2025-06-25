from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from devices.models import Device
from b_requests.models import BorrowRequest, ReturnRequest
from django.utils import timezone
from datetime import timedelta


@staff_member_required
def dashboard_view(request):
    user_count = User.objects.count()
    device_count = Device.objects.count()
    borrow_request_count = BorrowRequest.objects.count()
    return_request_count = ReturnRequest.objects.count()

    one_month_ago = timezone.now() - timedelta(days=30)

    type_count = (
        BorrowRequest.objects
        .filter(date_requested__gte=one_month_ago)
        .values('device__type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    device_type_labels = [x['device__type'] for x in type_count]
    device_type_data = [x['count'] for x in type_count]

    top_borrowers = (
        BorrowRequest.objects
        .filter(date_requested__gte=one_month_ago)
        .values('borrower__username')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    top_borrowers_labels = [x['borrower__username'] for x in top_borrowers]
    top_borrowers_data = [x['count'] for x in top_borrowers]

    context = {
        "user_count": user_count,
        "device_count": device_count,
        "borrow_request_count": borrow_request_count,
        "return_request_count": return_request_count,
        "device_type_labels": device_type_labels,
        "device_type_data": device_type_data,
        "top_borrowers_labels": top_borrowers_labels,
        "top_borrowers_data": top_borrowers_data,
    }
    return render(request, 'main/dashboard.html', context)


def home_view(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('devices:device-list')
        else:
            return redirect('accounts:login')
