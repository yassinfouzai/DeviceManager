from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BorrowRequestForm, ReturnRequestForm
from .models import BorrowRequest, ReturnRequest
from django.utils.dateformat import format
from devices.models import Device
import datetime


@staff_member_required
def return_detail_view(request, pk):
    return_request = get_object_or_404(ReturnRequest, pk=pk)

    if request.method == 'POST':
        if 'approve' in request.POST:
            return_request.approved = True
            return_request.save()

            device = return_request.device
            device.location = 'Admin'
            if return_request.condition == 'good':
                device.status = Device.Status.AVAILABLE
            elif return_request.condition == 'broken':
                device.status = Device.Status.BROKEN
            else:
                device.status = Device.Status.MISSING
            device.save()
        elif 'reject' in request.POST:
            return_request.delete()
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
            borrow_request.approved = True
            borrow_request.save()

            device = borrow_request.device
            device.location = borrow_request.borrower.username
            device.status = Device.Status.BORROWED
            device.save()
        elif 'reject' in request.POST:
            borrow_request.delete()
        return redirect('requests:request-list')

    context = {
        'request_obj': borrow_request
    }
    return render(request, 'b_requests/borrow_request_detail.html', context)


@staff_member_required
def request_list_view(request):
    borrows = BorrowRequest.objects.all()
    returns = ReturnRequest.objects.all()
    context = {"borrows": borrows, "returns": returns}
    return render(request, "b_requests/request_list.html", context)


@login_required
def borrow_request_view(request, id):
    device = get_object_or_404(Device, id=id)
    today = datetime.date.today()

    reservations = BorrowRequest.objects.filter(device=device, approved=True)
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

    borrow_request = BorrowRequest.objects.filter(device=device, borrower=request.user, approved=True).first()

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
