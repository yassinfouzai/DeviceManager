from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BorrowRequestForm, ReturnRequestForm
from .models import BorrowRequest, ReturnRequest
from django.utils.dateformat import format
from devices.models import Device
import datetime
from django.contrib import messages

@staff_member_required
def return_detail_view(request, pk):
    return_request = get_object_or_404(ReturnRequest, pk=pk)

    if request.method == 'POST':
        if 'approve' in request.POST:
            return_request.review = ReturnRequest.Review.APPROVED
            return_request.save()

            device = return_request.device
            device.location = 'Admin'
            if return_request.condition == ReturnRequest.Condition.GOOD:
                device.status = Device.Status.AVAILABLE
            elif return_request.condition == ReturnRequest.Condition.BROKEN:
                device.status = Device.Status.BROKEN
            else:
                device.status = Device.Status.MISSING
            device.save()
        elif 'reject' in request.POST:
            return_request.review = ReturnRequest.Review.REJECTED
            return_request.save()

        return redirect('requests:request-list')

    context = {
        'request_obj': return_request
    }
    return render(request, 'b_requests/return_request_detail.html', context)


@staff_member_required
def borrow_detail_view(request, pk):
    borrow_request = get_object_or_404(BorrowRequest, pk=pk)

    if request.method == 'POST':
        if 'approve' in request.POST:
            borrow_request.review = BorrowRequest.Review.APPROVED
            borrow_request.save()

            device = borrow_request.device
            device.location = borrow_request.borrower.username
            device.status = Device.Status.BORROWED
            device.save()
        elif 'reject' in request.POST:
            borrow_request.review = BorrowRequest.Review.REJECTED
            borrow_request.save()
        return redirect('requests:request-list')

    context = {
        'request_obj': borrow_request
    }
    return render(request, 'b_requests/borrow_request_detail.html', context)


@staff_member_required
def request_list_view(request):
    borrows = BorrowRequest.objects.all()
    returns = ReturnRequest.objects.all()

    conditions_qs = ReturnRequest.objects.values('condition').distinct()
    conditions = [c['condition'].replace('condition-', '') for c in conditions_qs]

    btypes_qs = BorrowRequest.objects.values_list('device__type', flat=True).distinct()
    btypes = [t.replace('type-', '') for t in btypes_qs]

    rtypes_qs = ReturnRequest.objects.values_list('device__type', flat=True).distinct()
    rtypes = [t.replace('type-', '') for t in rtypes_qs]

    breviews_qs = BorrowRequest.objects.values('review').distinct()
    breviews = [br['review'].replace('review-', '') for br in breviews_qs]

    rreviews_qs = ReturnRequest.objects.values('review').distinct()
    rreviews = [rr['review'].replace('review-', '') for rr in rreviews_qs]

    context = {
        "borrows": borrows,
        "returns": returns,
        "breviews": breviews,
        "rreviews": rreviews,
        "conditions": conditions,
        "btypes": btypes,
        "rtypes": rtypes,
    }
    return render(request, "b_requests/request_list.html", context)



@login_required
def borrow_request_view(request, id):
    device = get_object_or_404(Device, id=id)
    today = datetime.date.today()

    reservations = BorrowRequest.objects.filter(device=device, review='approved')
    reserved_dates = set()

    for r in reservations:
        current = r.date_requested
        while current <= r.return_date:
            reserved_dates.add(current)
            current += datetime.timedelta(days=1)

    reserved_dates = sorted([d.isoformat() for d in reserved_dates])

    if request.method == 'POST':
        form = BorrowRequestForm(request.POST, min_date=today)
        form.instance.device = device
        form.instance.borrower = request.user
        if form.is_valid():
            form.save()
            return redirect('devices:device-list')
        else:
            messages.error(request, ("Invalid date!"))
    else:
        form = BorrowRequestForm(min_date=today)

    return render(request, 'b_requests/borrow_request.html', {
        'form': form,
        'device': device,
        'min_reservation_date': today,
        'reserved_dates': reserved_dates,
    })


@login_required
def return_request_view(request, id):
    device = get_object_or_404(Device, id=id)

    borrow_request = BorrowRequest.objects.filter(device=device, borrower=request.user, review='approved').first()

    if not borrow_request:
        return redirect('devices:device-detail', id=device.id)

    if request.method == 'POST':
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.borrower = request.user
            return_request.device = device
            return_request.save()
            return redirect('devices:device-list')
    else:
        form = ReturnRequestForm()

    return render(request, 'b_requests/return_request.html', {
        'form': form,
        'device': device,
    })
