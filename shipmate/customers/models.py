from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    note = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ExternalContacts(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="extra")
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = "External contact"
        verbose_name_plural = "External contacts"
