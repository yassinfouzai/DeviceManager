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

    def __str__(self):
        return f"Borrow: {self.borrower.username} → {self.device.name}"


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

    def __str__(self):
        return f"Return: {self.borrower.username} ← {self.device.name} ({self.condition})"
