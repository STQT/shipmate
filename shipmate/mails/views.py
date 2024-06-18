from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shipmate.contrib.centraldispatch import get_central_dispatch_price
from shipmate.contrib.models import TrailerTypeChoices
from shipmate.leads.models import Leads
from shipmate.mails.data import static_dict
from shipmate.mails.serializers import ModulesListSerializer, CDPriceSerializer
from shipmate.orders.models import Order
from shipmate.quotes.models import Quote


class StaticDictView(APIView):
    serializer_class = ModulesListSerializer(many=True)

    def get(self, request):
        serializer_data = ModulesListSerializer(static_dict, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)


class GetCDPriceAPIView(APIView):
    serializer_class = CDPriceSerializer

    def get(self, request, obj, guid):
        obj_mapper = {
            "quote": Quote,
            "leads": Leads,
            "order": Order
        }
        reverse_relation_mapper = {
            "quote": "quote_vehicles",
            "leads": "lead_vehicles",
            "order": "order_vehicles"
        }
        try:
            rel_obj: Leads = obj_mapper[obj].objects.get(guid=guid)
        except obj_mapper[obj].DoesNotExist:
            return Response({"obj": ["Object does not exists from DB"]}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"obj": ["Select only from: quote, leads, order"]}, status=status.HTTP_400_BAD_REQUEST)

        vehicles_list = getattr(rel_obj, reverse_relation_mapper[obj])
        data = get_central_dispatch_price(
            rel_obj.origin.zip,
            rel_obj.destination.zip,
            False if rel_obj.trailer_type == TrailerTypeChoices.OPEN else True,
            vehicles_list.all()[0].vehicle.vehicle_type if vehicles_list.all() else 1,
            vehicles_list.count()
        )
        collected_data = {
            'cargo': [],
            'route': [],
            'price': [],
            'accepted': [],
            'comparable': []
        }
        for i in data:
            for j in data[i]:
                if j == 5:
                    continue
                key = self.set_dict_key(i)
                collected_data[key].append(data[i][j])
            collected_data['title'] = i
        if not collected_data:
            return Response({"nodata": ["CD Price doesnt return data"]}, status=status.HTTP_204_NO_CONTENT)
        serializer_data = self.serializer_class(collected_data)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    def set_dict_key(self, key):
        mapper = {
            "Cargo": "cargo",
            "Route": "route",
            "Price": "price",
            "Accepted by Carrier?": "accepted"
        }
        try:
            return mapper[key]
        except KeyError:
            return "comparable"
