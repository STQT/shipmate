from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shipmate.mails.data import static_dict


class StaticDictView(APIView):
    def get(self, request):
        return Response(static_dict, status=status.HTTP_200_OK)
