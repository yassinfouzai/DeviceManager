from django.core.management.base import BaseCommand
from django.utils import timezone
from b_requests.models import BorrowRequest, ReturnRequest
from datetime import timedelta


class Command(BaseCommand):
    help = 'Delete BorrowRequest and ReturnRequest entries older than one month with PENDING or REJECTED review.'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=30)

        old_borrows = BorrowRequest.objects.filter(
            review__in=[BorrowRequest.Review.PENDING, BorrowRequest.Review.REJECTED],
            date_requested__lt=cutoff
        )
        old_returns = ReturnRequest.objects.filter(
            review__in=[ReturnRequest.Review.PENDING, ReturnRequest.Review.REJECTED],
            date_returned__lt=cutoff
        )

        borrows_count = old_borrows.count()
        returns_count = old_returns.count()

        old_borrows.delete()
        old_returns.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Deleted {borrows_count} old borrow requests and {returns_count} old return requests."
        ))
