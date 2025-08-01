from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from b_requests.models import BorrowRequest, ReturnRequest
from devices.models import Device
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully!!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"{field.label}: {error}")
        for error in form.non_field_errors():
            messages.error(self.request, error)
        return super().form_invalid(form)


def get_unique_borrow_requests_by_device(borrow_requests):
    seen_devices = set()
    unique_requests = []

    for request in reversed(borrow_requests):
        device_id = request.device_id
        if device_id not in seen_devices:
            unique_requests.append(request)
            seen_devices.add(device_id)

    return list(reversed(unique_requests))


@login_required
def profile_view(request):
    borrow_requests = BorrowRequest.objects.filter(borrower=request.user)
    return_requests = ReturnRequest.objects.filter(borrower=request.user)
    approved_borrows = get_unique_borrow_requests_by_device(BorrowRequest.objects.filter(
        borrower=request.user,
        review='approved',
        device__location=request.user
    ))

    conditions_qs = ReturnRequest.objects.values('condition').distinct().filter(borrower=request.user)
    conditions = [c['condition'].replace('condition-', '') for c in conditions_qs]

    btypes_qs = BorrowRequest.objects.values_list('device__type', flat=True).distinct().filter(borrower=request.user)
    btypes = [t.replace('type-', '') for t in btypes_qs]

    rtypes_qs = ReturnRequest.objects.values_list('device__type', flat=True).distinct().filter(borrower=request.user)
    rtypes = [t.replace('type-', '') for t in rtypes_qs]

    breviews_qs = BorrowRequest.objects.values('review').distinct().filter(borrower=request.user)
    breviews = [br['review'].replace('review-', '') for br in breviews_qs]

    rreviews_qs = ReturnRequest.objects.values('review').distinct().filter(borrower=request.user)
    rreviews = [rr['review'].replace('review-', '') for rr in rreviews_qs]

    types_qs = Device.objects.values('type').distinct().filter(location=request.user)
    types = [t['type'].replace('type-', '') for t in types_qs]

    context = {
        "borrows": borrow_requests,
        "returns": return_requests,
        "approves": approved_borrows,
        "types": types,
        "btypes": btypes,
        "rtypes": rtypes,
        "breviews": breviews,
        "rreviews": rreviews,
        "conditions": conditions,
    }
    return render(request, 'accounts/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ("Try again!"))
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html', {})
