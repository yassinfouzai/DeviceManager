from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from b_requests.models import BorrowRequest, ReturnRequest


@login_required
def profile_view(request):
    borrow_requests = BorrowRequest.objects.filter(borrower=request.user)
    return_requests = ReturnRequest.objects.filter(borrower=request.user)
    approved_borrows = BorrowRequest.objects.filter(
        borrower=request.user,
        approved=True,
        device__location=request.user
    )

    context = {
        "borrows": borrow_requests,
        "returns": return_requests,
        "approves": approved_borrows,
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
