from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from b_requests.models import BorrowRequest, ReturnRequest
from b_requests.models import ArchivedBorrowRequest, ArchivedReturnRequest


class Command(BaseCommand):
    help = 'Archive BorrowRequest and ReturnRequest entries older than one month with PENDING or REJECTED review.'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=30)

        # archive old borrow requests
        old_borrows = BorrowRequest.objects.filter(
            review__in=[BorrowRequest.Review.PENDING, BorrowRequest.Review.REJECTED],
            date_requested__lt=cutoff
        )

        borrows_archived = 0
        for req in old_borrows:
            ArchivedBorrowRequest.objects.create(
                original_id=req.id,
                borrower=req.borrower,
                device=req.device,
                date_requested=req.date_requested,
                return_date=req.return_date,
                review=req.review,
                date_reviewed=req.date_reviewed,
                seen=req.seen
            )
            req.delete()
            borrows_archived += 1

        # archive old return requests
        old_returns = ReturnRequest.objects.filter(
            review__in=[ReturnRequest.Review.PENDING, ReturnRequest.Review.REJECTED],
            date_returned__lt=cutoff
        )

        returns_archived = 0
        for req in old_returns:
            ArchivedReturnRequest.objects.create(
                original_id=req.id,
                borrower=req.borrower,
                device=req.device,
                date_returned=req.date_returned,
                condition=req.condition,
                feedback=req.feedback,
                review=req.review,
                date_reviewed=req.date_reviewed,
                seen=req.seen
            )
            req.delete()
            returns_archived += 1

        self.stdout.write(self.style.SUCCESS(
            f"Archived {borrows_archived} borrow requests and {returns_archived} return requests older than 30 days."
        ))

