import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str) and data.startswith('data:image'):
            # Parse the base64 string
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # Guess file extension

            # Decode the image
            imgstr = base64.b64decode(imgstr)
            # Generate file name
            file_name = f"{uuid.uuid4()}.{ext}"
            data = ContentFile(imgstr, name=file_name)

        return super().to_internal_value(data)


class ReassignSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    reason = serializers.CharField()


class ArchiveSerializer(serializers.Serializer):
    reason = serializers.CharField()
