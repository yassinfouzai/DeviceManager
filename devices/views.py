from django.shortcuts import render, get_object_or_404
from .models import Device
from django.contrib.auth.decorators import login_required
from b_requests.models import BorrowRequest, ReturnRequest

@login_required
def device_detail_view(request, id):
    obj = get_object_or_404(Device, id=id)

    has_requested_borrow = BorrowRequest.objects.filter(
        device=obj,
        borrower=request.user,
        review=BorrowRequest.Review.PENDING
    ).exists()

    has_requested_return = ReturnRequest.objects.filter(
        device=obj,
        borrower=request.user,
        review=ReturnRequest.Review.PENDING
    ).exists()

    is_borrowed_by_user = BorrowRequest.objects.filter(
        device=obj,
        borrower=request.user,
        review=BorrowRequest.Review.APPROVED
    ).exists()

    context = {
        "object": obj,
        "has_requested_borrow": has_requested_borrow,
        "has_requested_return": has_requested_return,
        "is_borrowed_by_user": is_borrowed_by_user,
    }

    return render(request, "devices/device_detail.html", context)


@login_required
def device_list_view(request):
    queryset = Device.objects.all()
    types = Device.objects.values('type').distinct()
    types = [t['type'].replace('type-', '') for t in types]
    status = Device.objects.values('status').distinct()
    status = [s['status'].replace('status-', '') for s in status]
    context = {
        "object_list": queryset,
        "types": types,
        "status": status,
    }

    return render(request, "devices/device_list.html", context)
