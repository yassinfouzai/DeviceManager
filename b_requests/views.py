from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BorrowRequestForm, ReturnRequestForm
from .models import BorrowRequest, ReturnRequest
from devices.models import Device
import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from main.utils import notify_user
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


@staff_member_required
@require_POST
def mark_seen(request, request_type, id):
    try:
        if request_type == 'borrow':
            obj = BorrowRequest.objects.get(id=id)
        elif request_type == 'return':
            obj = ReturnRequest.objects.get(id=id)
        else:
            return JsonResponse({'error': 'Invalid request type'}, status=400)

        obj.seen = True
        obj.save()

        return JsonResponse({'status': 'success'})

    except (BorrowRequest.DoesNotExist, ReturnRequest.DoesNotExist):
        return JsonResponse({'error': f'{request_type.capitalize()}Request not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def return_detail_view(request, pk):
    return_request = get_object_or_404(ReturnRequest, pk=pk)

    if request.method == 'POST':
        user = return_request.borrower
        user_email = user.email
        device_name = return_request.device.name
        subject = ''
        message = ''

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

            subject = f"Return Request Approved – {device_name}"
            message = (
                f"Dear {user.username},\n\n"
                f"Your return of the device '{device_name}' has been approved.\n"
                f"The device status was recorded as: {return_request.get_condition_display()}.\n\n"
                "Thank you for returning it.\n\n"
                "Best regards,\n"
                "Device Management Team"
            )

            # WS
            notify_user(user.id, f"Your return request for '{device_name}' has been approved.")

        elif 'reject' in request.POST:
            return_request.review = ReturnRequest.Review.REJECTED
            return_request.save()

            subject = f"Return Request Rejected – {device_name}"
            message = (
                f"Dear {user.username},\n\n"
                f"Your return request for the device '{device_name}' has been rejected.\n"
                "Please contact the administration for clarification.\n\n"
                "Best regards,\n"
                "Device Management Team"
            )

            # WS
            notify_user(user.id, f"Your borrow request for '{device_name}' has been rejected.")

        # Send the email if a valid email exists
        if user_email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )

        return HttpResponse("Success", status=204)

    context = {
        'request_obj': return_request
    }
    return render(request, 'b_requests/return_request_detail.html', context)



@staff_member_required
def borrow_detail_view(request, pk):
    borrow_request = get_object_or_404(BorrowRequest, pk=pk)

    if request.method == 'POST':
        user = borrow_request.borrower
        user_email = user.email
        device_name = borrow_request.device.name
        subject = ''
        message = ''

        if 'approve' in request.POST:
            borrow_request.review = BorrowRequest.Review.APPROVED
            borrow_request.save()

            device = borrow_request.device
            device.location = borrow_request.borrower.username
            device.status = Device.Status.BORROWED
            device.save()

            # Email content
            subject = f"Your borrow request for '{device_name}' has been approved"
            message = (
                f"Dear {borrow_request.borrower.username},\n\n"
                f"Your request to borrow the device '{device_name}' has been approved.\n"
                "Please make arrangements to collect the device.\n\n"
                "Best regards,\n"
                "Device Management Team"
            )

            # WS
            notify_user(user.id, f"Your borrow request for '{device_name}' has been approved.")

        elif 'reject' in request.POST:
            borrow_request.review = BorrowRequest.Review.REJECTED
            borrow_request.save()

            # Email content
            subject = f"Your borrow request for '{device_name}' has been rejected"
            message = (
                f"Dear {borrow_request.borrower.username},\n\n"
                f"Unfortunately, your request to borrow the device '{device_name}' has been rejected.\n"
                "If you have any questions, please contact the administrator.\n\n"
                "Best regards,\n"
                "Device Management Team"
            )

            # WS
            notify_user(user.id, f"Your borrow request for '{device_name}' has been rejected.")

        if user_email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )

        return HttpResponse("Success", status=204)

    context = {
        'request_obj': borrow_request
    }
    return render(request, 'b_requests/borrow_request_detail.html', context)


@staff_member_required
def request_list_view(request):
    borrows = BorrowRequest.objects.all()
    returns = ReturnRequest.objects.all()

    unseed_borrows = BorrowRequest.objects.filter(seen=False).count()
    unseed_returns = ReturnRequest.objects.filter(seen=False).count()

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

        # Filters
        "breviews": breviews,
        "rreviews": rreviews,
        "conditions": conditions,
        "btypes": btypes,
        "rtypes": rtypes,

        # Notifications
        "unseed_borrows": unseed_borrows,
        "unseed_returns": unseed_returns,
    }

    return render(request, "b_requests/request_list.html", context)


@login_required
def borrow_request_view(request, id):
    device = get_object_or_404(Device, id=id)
    today = datetime.date.today()

    reservations = BorrowRequest.objects.filter(device=device, review='approved')
    reserved_dates = set()

    for r in reservations:
        actual_return = ReturnRequest.objects.filter(device=device, borrower=r.borrower).order_by('-date_returned').first()
        end_date = actual_return.date_returned.date() if actual_return else r.return_date

        current = r.date_requested
        while current <= end_date:
            reserved_dates.add(current)
            current += datetime.timedelta(days=1)

    reserved_dates = sorted([d.isoformat() for d in reserved_dates])

    if request.method == 'POST':
        form = BorrowRequestForm(request.POST, min_date=today)
        form.instance.device = device
        form.instance.borrower = request.user

        if form.is_valid():
            form.save()

            # Notify superuser
            User = get_user_model()
            superuser = User.objects.filter(is_superuser=True).first()
            notify_user(superuser.id, f"{request.user} requested to borrow for '{device}'.")

            if request.headers.get('HX-Request'):
                success_html = "<p class='text-green-600 font-semibold'>Borrow request submitted successfully.</p>"
                return HttpResponse(success_html)
            else:
                messages.success(request, "Borrow request submitted successfully.")
                return redirect('some-view-name')

        else:
            if request.headers.get('HX-Request'):
                error_html = render_to_string('partials/form_errors.html', {'form': form})
                return HttpResponse(error_html, status=400)
            else:
                messages.error(request, form.errors.as_text())

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
        if request.headers.get('HX-Request'):
            return HttpResponse(
                render_to_string('partials/error_message.html', {
                    'message': 'You do not have an approved borrow request for this device.'
                }),
                status=400
            )
        return redirect('devices:device-detail', id=device.id)

    if request.method == 'POST':
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.borrower = request.user
            return_request.device = device
            return_request.save()

            # Notify superuser
            User = get_user_model()
            superuser = User.objects.filter(is_superuser=True).first()
            notify_user(superuser.id, f"{request.user} requested to return for '{device}'.")

            if request.headers.get('HX-Request'):
                return HttpResponse(
                    "<p class='text-green-600 font-semibold'>Return request submitted successfully.</p>",
                    status=200
                )
            else:
                messages.success(request, "Return request submitted successfully.")
                return redirect('devices:device-detail', id=device.id)
        else:
            if request.headers.get('HX-Request'):
                return HttpResponse(
                    render_to_string('b_requests/return_request.html', {'form': form, 'device': device}),
                    status=400
                )
            else:
                messages.error(request, form.errors.as_text())

    else:
        form = ReturnRequestForm()

    return render(request, 'b_requests/return_request.html', {
        'form': form,
        'device': device,
    })
