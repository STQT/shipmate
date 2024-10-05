from django.contrib.auth import get_user_model
from django.db import models

from shipmate.utils.models import BaseLog

User = get_user_model()


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
    logo = models.ImageField(upload_to="logos", blank=True, null=True)

    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyInfoLog(BaseLog):
    company_info = models.ForeignKey("CompanyInfo", on_delete=models.CASCADE, related_name="logs")


class MerchantStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class MerchantTypeChoices(models.TextChoices):
    AUTHORIZE = "authorize", "Authorize"
    FIRSTDATA = "firstdata", "Firstdata"
    PayPal = "paypal", "PayPal"


class Merchant(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(choices=MerchantStatusChoices.choices, max_length=8)
    merchant_type = models.CharField(choices=MerchantTypeChoices.choices, max_length=20)

    authorize_login = models.CharField(max_length=50, null=True, blank=True)
    authorize_password = models.CharField(max_length=50, null=True, blank=True)
    authorize_pin_code = models.CharField(max_length=255, null=True, blank=True)

    firstdata_gateway_id = models.CharField(max_length=50, null=True, blank=True)
    firstdata_password = models.CharField(max_length=50, null=True, blank=True)
    firstdata_key_id = models.CharField(max_length=50, null=True, blank=True)
    firstdata_hmac_key = models.CharField(max_length=50, null=True, blank=True)

    paypal_secret_key = models.CharField(max_length=50, null=True, blank=True)

    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)
    created_on = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", editable=False,
                                   null=True, blank=True)

    def __str__(self):
        return self.name


class MerchantLog(BaseLog):
    merchant = models.ForeignKey("Merchant", on_delete=models.CASCADE, related_name="logs")


class VoIPStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class VoIPTypeChoices(models.TextChoices):
    ZOOM = "zoom", "Zoom"
    DIALPAD = "dialpad", "Dialpad"
    RINGCENTRAL = "ringcentral", "Ringcentral"


class VoIP(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(choices=VoIPStatusChoices.choices, max_length=8)
    voip_type = models.CharField(choices=VoIPTypeChoices.choices, max_length=20)
    api = models.CharField(max_length=255)

    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_on = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", editable=False)


class VoIPLog(BaseLog):
    voip = models.ForeignKey("VoIP", on_delete=models.CASCADE, related_name="logs")


class TemplateStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class TemplateTypeChoices(models.TextChoices):
    SMS = "sms", "SMS"
    EMAIL = "email", "Email"


class Template(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=500, null=True, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=8, choices=TemplateStatusChoices.choices)
    template_type = models.CharField(max_length=5, choices=TemplateTypeChoices.choices)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TemplateLog(BaseLog):
    template = models.ForeignKey("Template", on_delete=models.CASCADE, related_name="logs")


class PaymentAppStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class PaymentAppTypeChoices(models.TextChoices):
    ZELLE = "zelle", "Zelle"
    PAYPAL = "paypal", "PayPal"
    CASHAPP = "cashapp", "CashApp"
    VENMO = "venmo", "Venmo"


class PaymentApp(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=8, choices=PaymentAppStatusChoices.choices)
    payment_type = models.CharField(max_length=10, choices=PaymentAppTypeChoices.choices)
    account_name = models.CharField(max_length=255)
    account_username = models.CharField(max_length=255)
    link = models.URLField(max_length=255, blank=True, null=True)
    qr_code = models.ImageField(upload_to="payments", blank=True, null=True)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PaymentAppLog(BaseLog):
    payment = models.ForeignKey("PaymentApp", on_delete=models.CASCADE, related_name="logs")


class LeadParsingGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LeadParsingItem(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(LeadParsingGroup, on_delete=models.CASCADE, related_name='values')

    def __str__(self):
        return self.name


class LeadParsingValue(models.Model):
    item = models.ForeignKey(LeadParsingItem, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value
