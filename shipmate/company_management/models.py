from django.db import models


class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)
    mainline = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name
