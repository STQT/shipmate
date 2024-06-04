from rest_framework import serializers
from .models import CompanyInfo


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = ['name', 'mainline', 'fax', 'email', 'address']
