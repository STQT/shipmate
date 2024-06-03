from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages

from shipmate.contract.models import Ground, Hawaii, International


class BaseContractForm(forms.ModelForm):
    class Meta:
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance
        instance.is_default = cleaned_data.get("is_default")
        instance.validate_single_default()
        return cleaned_data


class BaseContractAdmin(admin.ModelAdmin):
    form = BaseContractForm  # This should be set in the subclass
    list_display = ["name", "status", "is_default"]

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.error(request, e.message)

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except ValidationError as e:
            messages.error(request, e.message)


class GroundAdmin(BaseContractAdmin):
    form = BaseContractForm


class HawaiiAdmin(BaseContractAdmin):
    form = BaseContractForm


class InternationalAdmin(BaseContractAdmin):
    form = BaseContractForm


admin.site.register(Ground, GroundAdmin)
admin.site.register(Hawaii, HawaiiAdmin)
admin.site.register(International, InternationalAdmin)
