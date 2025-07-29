from django.db import models
from django.contrib.auth.models import User
from devices.models import Device
from django.utils import timezone


class BorrowRequest(models.Model):
    class Review(models.TextChoices):
        APPROVED = 'approved', 'Approved'
        PENDING = 'pending', 'Pending'
        REJECTED = 'rejected', 'Rejected'
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='borrow_requests')
    date_requested = models.DateField(default=timezone.now)
    return_date = models.DateField(null=False, blank=False)
    review = models.CharField(max_length=20, choices=Review.choices, default=Review.PENDING)
    date_reviewed = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Borrow: {self.borrower.username} → {self.device.name}"

    def save(self, *args, **kwargs):
        if self.review == self.Review.REJECTED and self.date_reviewed is None:
            self.date_reviewed = timezone.now()
        super().save(*args, **kwargs)


class ReturnRequest(models.Model):
    class Condition(models.TextChoices):
        GOOD = 'good', 'Good'
        BROKEN = 'broken', 'Broken'
        MISSING = 'missing', 'Missing'

    class Review(models.TextChoices):
        APPROVED = 'approved', 'Approved'
        PENDING = 'pending', 'Pending'
        REJECTED = 'rejected', 'Rejected'

    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_requests')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='return_requests')
    date_returned = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    feedback = models.TextField(blank=True, null=True)
    review = models.CharField(max_length=20, choices=Review.choices, default=Review.PENDING)
    date_reviewed = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Return: {self.borrower.username} ← {self.device.name} ({self.condition})"

    def save(self, *args, **kwargs):
        if self.review == self.Review.REJECTED and self.date_reviewed is None:
            self.date_reviewed = timezone.now()
        super().save(*args, **kwargs)


class ArchivedBorrowRequest(models.Model):
    original_id = models.IntegerField()  # Track original BorrowRequest ID
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_borrow_requests')
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, related_name='archived_borrow_requests')
    date_requested = models.DateField()
    return_date = models.DateField()
    review = models.CharField(max_length=20, choices=BorrowRequest.Review.choices)
    date_reviewed = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived Borrow: {self.borrower.username if self.borrower else 'Deleted User'} → {self.device.name if self.device else 'Deleted Device'}"


class ArchivedReturnRequest(models.Model):
    original_id = models.IntegerField()
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_return_requests')
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, related_name='archived_return_requests')
    date_returned = models.DateTimeField()
    condition = models.CharField(max_length=20, choices=ReturnRequest.Condition.choices)
    feedback = models.TextField(blank=True, null=True)
    review = models.CharField(max_length=20, choices=ReturnRequest.Review.choices)
    date_reviewed = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived Return: {self.borrower.username if self.borrower else 'Deleted User'} ← {self.device.name if self.device else 'Deleted Device'}"
