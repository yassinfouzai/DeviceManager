from .models import BorrowRequest, ReturnRequest


def unseen_request_counts(request):
    if not request.user.is_authenticated:
        return {}

    unseen_borrows = BorrowRequest.objects.filter(seen=False).count()
    unseen_returns = ReturnRequest.objects.filter(seen=False).count()

    return {
        'unseen_borrows': unseen_borrows,
        'unseen_returns': unseen_returns,
    }

