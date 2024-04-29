from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_email = models.EmailField()
    status = models.BooleanField(default=True)
    company_branches = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Branch(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_email = models.EmailField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
