from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Merchant, MerchantLog, CompanyInfoLog, CompanyInfo, VoIP, VoIPLog, Template, TemplateLog, \
    PaymentApp, PaymentAppLog
from ..contrib.logging import log_update, store_old_values

User = get_user_model()


@receiver(pre_save, sender=Merchant)
def log_merchant_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Merchant)
def log_merchant_update(sender, instance, created, **kwargs):
    kwargs['is_secured'] = True
    log_update(sender, instance, created, MerchantLog, "merchant", **kwargs)


@receiver(pre_save, sender=CompanyInfo)
def log_company_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=CompanyInfo)
def log_company_info_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, CompanyInfoLog, "company_info", **kwargs)


@receiver(pre_save, sender=VoIP)
def log_voip_user_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=VoIP)
def log_distribution_update(sender, instance, created, **kwargs):
    kwargs['is_secured'] = True
    log_update(sender, instance, created, VoIPLog, "voip", **kwargs)


@receiver(pre_save, sender=Template)
def log_template_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=Template)
def log_template_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, TemplateLog, "template", **kwargs)


@receiver(pre_save, sender=PaymentApp)
def log_paymentapp_data(sender, instance, **kwargs):
    store_old_values(sender, instance, **kwargs)


@receiver(post_save, sender=PaymentApp)
def log_paymentapp_update(sender, instance, created, **kwargs):
    log_update(sender, instance, created, PaymentAppLog, "payment", **kwargs)
