from django.db import models
from django.contrib.auth.models import AbstractUser
from company.models import Company, Branch


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    ACCESS_LEVEL_CHOICES = (
        (1, 'Manager'),
        (2, 'Cashier'),
    )
    MANAGING_CHOICES = (
        (1, 'Finance'),
        (2, 'Stock Manager'),
    )

    access_level = models.IntegerField(
        choices=ACCESS_LEVEL_CHOICES,
        null=True,
        blank=True
    )
    managing_level = models.IntegerField(
        choices=MANAGING_CHOICES,
        null=True,
        blank=True
    )

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')

    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='company'
    )

    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='branch'
    )

    def __str__(self):
        return self.username
