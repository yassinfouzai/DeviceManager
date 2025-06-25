from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BorrowRequestForm, ReturnRequestForm
from .models import BorrowRequest, ReturnRequest
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

    latest_approved = BorrowRequest.objects.filter(
        device=device,
        approved=True
    ).order_by('-return_date').first()

    today = datetime.date.today()
    if latest_approved and latest_approved.return_date >= today:
        min_reservation_date = latest_approved.return_date + datetime.timedelta(days=1)
    else:
        min_reservation_date = today

    if request.method == 'POST':
        form = BorrowRequestForm(request.POST, min_date=min_reservation_date)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.device = device
            borrow_request.borrower = request.user
            borrow_request.save()
            return redirect('devices:device-list')
    else:
        form = BorrowRequestForm(min_date=min_reservation_date)

    return render(request, 'b_requests/borrow_request.html', {
        'form': form,
        'device': device,
        'min_reservation_date': min_reservation_date,
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
