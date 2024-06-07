from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shipmate.mails.data import static_dict
from shipmate.mails.serializers import ModulesListSerializer


class StaticDictView(APIView):
    serializer_class = ModulesListSerializer(many=True)

    def get(self, request):
        serializer_data = ModulesListSerializer(static_dict, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
