from django.db import models

from shipmate.utils.models import BaseLog


class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    mainline = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField()
    support_email = models.EmailField()
    accounting_email = models.EmailField()
    address = models.TextField()
    mon_fri = models.CharField(max_length=50)
    saturday = models.CharField(max_length=50)
    sunday = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CompanyInfoLog(BaseLog):
    company_info = models.ForeignKey("CompanyInfo", on_delete=models.CASCADE, related_name="logs")
