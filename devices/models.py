from django.db import models


class Device(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        BORROWED = 'borrowed', 'Borrowed'
        BROKEN = 'broken', 'Broken'
        MISSING = 'missing', 'Missing'

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    dimension = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    location = models.CharField(max_length=100, default='Admin')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

